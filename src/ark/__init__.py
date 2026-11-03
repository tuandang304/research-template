"""Agent Research Kit (ark) — a reproducible research project package.

Import the pieces you need:

    from ark import config, set_seed, get_logger, start_run
"""

from ark.config import DATA_DIR, PROJECT_ROOT, RESULTS_DIR, config
from ark.logging import get_logger
from ark.seed import set_seed
from ark.tracking import start_run

__version__ = "0.2.0"

__all__ = [
    "__version__",
    "config",
    "PROJECT_ROOT",
    "DATA_DIR",
    "RESULTS_DIR",
    "get_logger",
    "set_seed",
    "start_run",
]
