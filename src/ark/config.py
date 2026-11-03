"""Central configuration: project paths and settings loaded from ``config.yaml``.

Everything here is resolved relative to the repository root, so paths work the
same whether you run a script, a notebook, or a test — no ``../..`` juggling.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

# The repo root is two parents up from this file: src/ark/config.py -> repo/
PROJECT_ROOT: Path = Path(__file__).resolve().parents[2]

DATA_DIR: Path = PROJECT_ROOT / "data"
RAW_DATA_DIR: Path = DATA_DIR / "raw"
PROCESSED_DATA_DIR: Path = DATA_DIR / "processed"
EXTERNAL_DATA_DIR: Path = DATA_DIR / "external"

RESULTS_DIR: Path = PROJECT_ROOT / "results"
FIGURES_DIR: Path = RESULTS_DIR / "figures"
TABLES_DIR: Path = RESULTS_DIR / "tables"

EXPERIMENTS_DIR: Path = PROJECT_ROOT / "experiments"

_CONFIG_FILE: Path = PROJECT_ROOT / "config.yaml"


@dataclass(frozen=True)
class Config:
    """Project-wide settings. Values are read from ``config.yaml`` if present."""

    seed: int = 42
    log_level: str = "INFO"
    experiment: str = "example_experiment"
    params: dict[str, Any] = field(default_factory=dict)
    extra: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def load(cls, path: Path = _CONFIG_FILE) -> Config:
        if not path.exists():
            return cls()
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        known = {"seed", "log_level", "experiment", "params"}
        return cls(
            seed=int(data.get("seed", 42)),
            log_level=str(data.get("log_level", "INFO")),
            experiment=str(data.get("experiment", "example_experiment")),
            params=dict(data.get("params") or {}),
            extra={k: v for k, v in data.items() if k not in known},
        )


# Import-time singleton — `from ark.config import config`
config: Config = Config.load()
