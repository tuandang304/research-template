"""Smoke tests — verify the template's plumbing works out of the box."""

from __future__ import annotations

from pathlib import Path

import ark
from ark import config, get_logger, set_seed
from ark.config import PROJECT_ROOT


def test_version() -> None:
    assert isinstance(ark.__version__, str)


def test_config_defaults() -> None:
    assert config.seed == 42
    assert config.log_level


def test_project_root_is_repo() -> None:
    assert (PROJECT_ROOT / "pyproject.toml").exists()


def test_set_seed_is_deterministic() -> None:
    import random

    set_seed(123)
    a = [random.random() for _ in range(3)]
    set_seed(123)
    b = [random.random() for _ in range(3)]
    assert a == b


def test_logger() -> None:
    log = get_logger("test")
    log.info("logging works")


def test_paths_are_pathlib() -> None:
    from ark.config import DATA_DIR, RESULTS_DIR

    assert isinstance(DATA_DIR, Path)
    assert isinstance(RESULTS_DIR, Path)


def test_config_names_an_experiment_with_run() -> None:
    import importlib

    module = importlib.import_module(f"experiments.{config.experiment}")
    assert callable(module.run)
    assert isinstance(config.params, dict)


def test_summary_writes_metrics(tmp_path, monkeypatch, capsys) -> None:
    import json

    from ark import tracking

    monkeypatch.setattr(tracking, "RESULTS_DIR", tmp_path)
    monkeypatch.setattr(tracking, "PROJECT_ROOT", tmp_path)
    with tracking.start_run("test", {"lr": 0.1}) as run:
        run.log({"loss": 1.0}, step=0)
        run.summary({"accuracy": 0.5})

    assert json.loads((tmp_path / "metrics.json").read_text()) == {"accuracy": 0.5}
    assert 'summary: {"accuracy": 0.5}' in capsys.readouterr().out
