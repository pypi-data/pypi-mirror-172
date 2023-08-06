"""Global constants and shared functions in common."""
from __future__ import annotations

import sys
from typing import TypedDict

# third-party imports
import loguru
import typer
from loguru import logger
from statsdict import StatsDict  # type: ignore

# module imports
from . import __doc__ as docstring
from .rcsb_cache import RCSBCache


# global constants
DEFAULT_STDERR_LOG_LEVEL = "INFO"
NO_LEVEL_BELOW = 30  # Don't print level for messages below this level
NAME = "zeigen"
ID_FIELD = "rcsb_id"
SUB_FIELD = "sub"
NEIGHBOR_FILE = "neighbors.tsv"
METADATA_FILE = "metadata.json"


class GlobalState(TypedDict):
    """Dictionary of global state variables."""

    verbose: bool
    log_level: str


STATE: GlobalState = {"verbose": False, "log_level": DEFAULT_STDERR_LOG_LEVEL}


def _stderr_format_func(record: loguru.Record) -> str:
    """Do level-sensitive formatting."""
    if record["level"].no < NO_LEVEL_BELOW:
        return "<level>{message}</level>\n"
    return "<level>{level}</level>: <level>{message}</level>\n"


logger.remove()
logger.add(sys.stderr, level=STATE["log_level"], format=_stderr_format_func)
APP = typer.Typer(help=docstring, name=NAME)
STATS = StatsDict(logger=logger, app=APP, module_name=NAME)
RCSB_CACHE = RCSBCache(logger=logger, app=APP)
