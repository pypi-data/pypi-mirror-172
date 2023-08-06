"""For space rocks."""
from pathlib import Path

import rich
from rich import traceback

# pretty-print tracebacks with rich
traceback.install()

# ------
# Path definitions required throughout the code
PATH_CACHE = Path.home() / ".cache/rocks"
PATH_INDEX = PATH_CACHE / "index"
PATH_MAPPING = PATH_CACHE / "metadata_aster.json"
PATH_AUTHORS = PATH_CACHE / "ssodnet_biblio.json"

# rocks modules
# rocks.plots is lazy-loaded as it is expensive
from . import datacloud, ssodnet, utils, index

# Expose API to user
from .core import Rock
from .core import rocks_ as rocks
from .resolve import identify, id


# Dict to hold the asteroid name-number indices and mappings at runtime
INDEX = {}
MAPPINGS = {}

# ------
# Welcome to rocks
__version__ = "1.6.4"

GREETING = rf"""
                _
               | |
 _ __ ___   ___| | _____
| '__/ _ \ / __| |/ / __|
| | | (_) | (__|   <\__ \
|_|  \___/ \___|_|\_\___/

version: {__version__}
cache:   {PATH_CACHE}

It looks like this is the first time you run [green]rocks[/green].
Some metadata is required to be present in the cache directory.
[green]rocks[/green] will download it now.
"""


# ------
# Check for existence of index file and cache directory
if not PATH_INDEX.is_dir():

    rich.print(GREETING)

    # Just for a while
    if (Path.home() / ".cache/rocks/index.pkl").is_file():
        (Path.home() / ".cache/rocks/index.pkl").unlink()

    PATH_INDEX.mkdir(parents=True)
    index._build_index()

    rich.print("\nAll done. Find out more by running [green]$ rocks docs[/green]\n")
