#!/usr/bin/env python
"""Utility functions for rocks."""

from bs4 import BeautifulSoup
from functools import reduce
import json
import re
import shutil
import string
import tarfile
import urllib
import warnings
from functools import lru_cache

import numpy as np
import Levenshtein as lev
import requests
import rich
from rich.progress import track

import rocks


# ------
# Simplify error messages
def warning_on_one_line(message, category, filename, lineno, file=None, line=None):
    if "rocks/" in filename:
        return f"rocks: {message}\n"
    else:
        return f"{filename}:{lineno}: {category.__name__}: {message}\n"


warnings.formatwarning = warning_on_one_line


# ------
# ssoCard utility functions
def rgetattr(obj, attr):
    """Deep version of getattr. Retrieve nested attributes."""

    def _getattr(obj, attr):
        return getattr(obj, attr)

    return reduce(_getattr, [obj] + attr.split("."))


def get_unit(path_parameter: str) -> str:
    """Get unit from units JSON file.

    Parameters
    ----------
    path_parameter : str
        Path to the parameter in the mappings JSON tree.

    Returns
    -------
    str
        The unit of the requested parameter.
    """
    mappings = load_mappings()

    if "unit" in mappings[path_parameter]:
        unit = mappings[path_parameter]["unit"]
    else:
        unit = ""

    return unit


@lru_cache(maxsize=128)
def load_mappings():
    """Load SsODNet metadata mappings file from cache."""
    if not rocks.PATH_MAPPING.is_file():
        retrieve_metadata("mappings")

    with open(rocks.PATH_MAPPING, "r") as file_:
        rocks.MAPPINGS = json.load(file_)
    return rocks.MAPPINGS


# ------
# Numerical methods
def weighted_average(catalogue, parameter):
    """Computes weighted average of observable.

    Parameters
    ----------
    observable : np.ndarray
        Float values of observable
    error : np.ndarray
        Corresponding errors of observable.

    Returns
    -------
    float
        The weighted average.

    float
        The standard error of the weighted average.
    """
    catalogue = catalogue[catalogue[parameter] != 0]

    values = catalogue[parameter]

    if parameter in ["albedo", "diameter"]:
        preferred = catalogue[f"preferred_{parameter}"]

        if not any(preferred):
            preferred = ~preferred

        errors = catalogue[f"err_{parameter}_up"]
    else:
        preferred = catalogue["preferred"]
        errors = catalogue[f"err_{parameter}"]

    observable = np.array(values)[preferred]
    error = np.array(errors)[preferred]

    if all(np.isnan(value) for value in values) or all(
        np.isnan(error) for error in errors
    ):
        warnings.warn(
            f"{catalogue.name[0]}: The values or errors of property '{parameter}' are all NaN. Average failed."
        )
        return np.nan, np.nan

    # If no data was passed (happens when no preferred entry in table)
    if not observable.size:
        return (np.nan, np.nan)

    if len(observable) == 1:
        return (observable[0], error[0])

    if any(e == 0 for e in error):
        weights = np.ones(observable.shape)
        warnings.warn("Encountered zero in errors array. Setting all weights to 1.")
    else:
        # Compute normalized weights
        weights = 1 / np.array(error) ** 2

    # Compute weighted average and uncertainty
    avg = np.average(observable, weights=weights)

    # Kirchner Case II
    # http://seismo.berkeley.edu/~kirchner/Toolkits/Toolkit_12.pdf
    var_avg = (
        len(observable)
        / (len(observable) - 1)
        * (
            sum(w * o**2 for w, o in zip(weights, observable)) / sum(weights)
            - avg**2
        )
    )
    std_avg = np.sqrt(var_avg / len(observable))
    return avg, std_avg


# ------
# Misc
def retrieve_metadata(which):
    """Retrieve the metadata JSON files from SsODNet to the cache directory.

    Parameter
    ---------
    which : str
        Which metadata to retrieve. Choose from ['mappings', 'authors'].
    """

    if which not in ["mappings", "authors"]:
        raise ValueError

    URL = (
        "https://ssp.imcce.fr/data/ssodnet_biblio.json"
        if which == "authors"
        else "https://ssp.imcce.fr/data/metadata_aster.json"
    )

    response = requests.get(URL)

    if not response.ok:
        warnings.error(f"Retrieving {which} file failed with URL:\n{URL}")
        return

    metadata = response.json()

    if which == "mappings":
        metadata = metadata["display"]

    PATH_OUT = rocks.PATH_AUTHORS if which == "authors" else rocks.PATH_MAPPING

    with open(PATH_OUT, "w") as file_:
        json.dump(metadata, file_)


def cache_inventory():
    """Create lists of the cached ssoCards and datacloud catalogues.

    Returns
    -------
    list of tuple
        The SsODNet IDs and versions of the cached ssoCards.
    list of tuple
        The SsODNet IDs and names of the cached datacloud catalogues.
    """

    # Get all JSONs in cache
    cached_jsons = set(file_ for file_ in rocks.PATH_CACHE.glob("*.json"))

    cached_cards = []
    cached_catalogues = []

    for file_ in cached_jsons:

        # Is it metadata?
        if file_ == rocks.PATH_MAPPING:
            continue

        # Datacloud catalogue or ssoCard?
        if any(
            cat["ssodnet_name"] in str(file_)
            for cat in rocks.datacloud.CATALOGUES.values()
        ):
            *ssodnet_id, catalogue = file_.stem.split("_")
            ssodnet_id = "_".join(ssodnet_id)
        else:
            ssodnet_id = file_.stem
            catalogue = ""

        # Is it valid?
        with open(file_, "r") as ssocard:

            try:
                _ = json.load(ssocard)
            except json.decoder.JSONDecodeError:
                # Empty card or catalogue, remove it
                file_.unlink()
                continue

        # Append to inventory
        if catalogue:
            cached_catalogues.append((ssodnet_id, catalogue))
        else:
            cached_cards.append(ssodnet_id)

    return cached_cards, cached_catalogues


def clear_cache():
    """Remove the cached ssoCards and datacloud catalogues."""
    cards, catalogues = cache_inventory()

    for card in cards:
        PATH_CARD = rocks.PATH_CACHE / f"{card}.json"
        PATH_CARD.unlink()

    for catalogue in catalogues:
        PATH_CATALOGUE = rocks.PATH_CACHE / f"{'_'.join(catalogue)}.json"
        PATH_CATALOGUE.unlink()

    if rocks.PATH_MAPPING.is_file():
        rocks.PATH_MAPPING.unlink()


def update_datacloud_catalogues(cached_catalogues):
    for catalogue in set(catalogues[1] for catalogues in cached_catalogues):

        ids = [id_ for id_, cat in cached_catalogues if cat == catalogue]

        rocks.ssodnet.get_datacloud_catalogue(
            ids, catalogue, local=False, progress=True
        )


def confirm_identity(ids):
    """Confirm the SsODNet ID of the passed identifier. Retrieve the current
    ssoCard and remove the former one if the ID has changed.

    Parameters
    ----------
    ids : list
        The list of SsODNet IDs to confirm.
    """

    # Drop the named asteroids - their identity won't change
    ids = set(id_ for id_ in ids if not re.match(r"^[A-Za-z \(\)\_]*$", id_))

    if not ids:
        return  # nothing to do here
    elif len(ids) == 1:
        _, _, current_ids = rocks.identify(ids, return_id=True, local=False)
        current_ids = [current_ids]
    else:
        _, _, current_ids = zip(
            *rocks.identify(ids, return_id=True, local=False, progress=True)
        )

    # Swap the renamed ones
    updated = []

    for old_id, current_id in zip(ids, current_ids):

        if old_id == current_id:
            continue

        rich.print(f"{old_id} has been renamed to {current_id}. Swapping the ssoCards.")

        # Get new card and remove the old one
        rocks.ssodnet.get_ssocard(current_id, local=False)
        (rocks.PATH_CACHE / f"{old_id}.json").unlink()

        # This is now up-to-date
        updated.append(old_id)

    for id_ in updated:
        ids.remove(id_)


def retrieve_rocks_version():
    """Retrieve the current rocks version from the GitHub repository."""

    URL = "https://github.com/maxmahlke/rocks/blob/master/pyproject.toml?raw=True"

    try:
        response = requests.get(URL, timeout=10)
    except requests.exceptions.ReadTimeout:
        return ""

    if response.status_code == 200:
        version = re.findall(r"\d+\.\d+[\.\d]*", response.text)[0]
    else:
        version = ""

    return version


def find_candidates(id_):
    """Identify possible matches among all asteroid names based on Levenshtein distance.

    Parameters
    ----------
    id_ : str
        The user-provided asteroid identifier.

    Returns
    -------
    list of tuple
        The name-number pairs of possible matches.

    Notes
    -----
    The matches are found using the Levenshtein distance metric.
    """

    # Get list of named asteroids
    index = {}

    for char in string.ascii_lowercase:
        idx = rocks.index.get_index_file(char)
        index = {**index, **idx}

    # Use Levenshtein distance to identify potential matches
    candidates = []
    max_distance = 1  # found by trial and error
    id_ = rocks.resolve._reduce_id_for_local(id_)

    for name in index.keys():
        distance = lev.distance(id_, name)

        if distance <= max_distance:
            candidates.append(index[name][:-1])

    # Sort by number
    candidates = sorted(candidates, key=lambda x: x[1])
    return candidates


def list_candidate_ssos(id_):
    """Propose matches for failed id queries based on Levenshtein distance if the passed identifier is a name.

    Parameters
    ----------
    id_ : str
        The passed asteroid identifier.

    Note
    ----
    The proposed matches are printed to stdout.
    """

    # This only makes sense for named asteroids
    if not re.match(r"^[A-Za-z ]*$", id_):
        return

    candidates = rocks.utils.find_candidates(id_)

    if candidates:
        rich.print(
            f"\nCould {'this' if len(candidates) == 1 else 'these'} be the "
            f"{'rock' if len(candidates) == 1 else 'rocks'} you're looking for?"
        )

        for name, number in candidates:
            rich.print(f"{f'({number})':>8} {name}")


def cache_all_ssocards():
    """Retrieves all ssoCards and stores them in the cache directory.

    Warning: This will slow down the '$ rocks status' command considerably.
    """

    # Retrieve archive of ssoCards
    PATH_ARCHIVE = "/tmp/ssoCard-latest.tar.gz"

    URL = "https://ssp.imcce.fr/webservices/ssodnet/api/ssocard/ssoCard-latest.tar.bz2"

    response = requests.get(URL, stream=True)

    with open(PATH_ARCHIVE, "wb") as fp:
        shutil.copyfileobj(response.raw, fp)

    # Extract to the cache directory
    cards = tarfile.open(PATH_ARCHIVE, mode="r:bz2")
    members = cards.getmembers()

    for member in track(members, total=len(members), description="Unpacking ssoCards"):

        if not member.name.endswith(".json"):
            continue

        member.path = member.path.split("/")[-1]
        cards.extract(member, rocks.PATH_CACHE)


def get_citation_from_mpc(name):
    """Query asteroid information from MPC and extract citation from HTML response."""

    URL = f"https://minorplanetcenter.net/db_search/show_object?object_id={urllib.parse.quote_plus(str(name))}"

    soup = BeautifulSoup(requests.get(URL).text, "html.parser")

    citation = soup.find("div", {"id": "citation"})

    if citation is None:
        return None

    # Extract citation and do minor formatting
    citation = citation.find("br").next_sibling.next_sibling
    citation = citation.split("[")[0].strip().replace("  ", " ")
    return citation


def check_datasets(author):
    """Print dataset and publication matching 'author' as first-author name."""

    if not rocks.PATH_AUTHORS.is_file():
        rocks.utils.retrieve_metadata("authors")

    with open(rocks.PATH_AUTHORS, "r") as file_:
        ssodnet_biblio = json.load(file_)

    for category, datasets in ssodnet_biblio["ssodnet_biblio"]["datasets"].items():
        for dataset in datasets:
            if author.capitalize() in dataset["shortbib"]:
                print(f"  {dataset['shortbib']:<20} [{category}]")
