"""Metric tracking that OpenResearch can read back.

``start_run`` logs to `Trackio <https://github.com/gradio-app/trackio>`_ when it
is installed (``uv add trackio``), using the ``ORX_*`` and ``TRACKIO_PROJECT``
variables that ``orx exp run`` sets, so orx shows the charts beside the run and
``orx metrics <runId>`` can read them. Without Trackio it still logs to stdout.

``Run.summary`` prints one ``summary: {...}`` line and writes
``results/metrics.json``: the compact final result ``orx logs`` looks for.
"""

from __future__ import annotations

import json
import os
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any

from ark.config import PROJECT_ROOT, RESULTS_DIR
from ark.logging import get_logger

log = get_logger("tracking")


class Run:
    def __init__(self, trackio: Any | None) -> None:
        self._trackio = trackio

    def log(self, metrics: dict[str, float], step: int | None = None) -> None:
        """Log a step's metrics (loss, accuracy, ...)."""
        if self._trackio is not None:
            self._trackio.log(metrics, step=step)
        prefix = f"step {step} " if step is not None else ""
        log.info("%smetric: %s", prefix, json.dumps(metrics))

    def summary(self, metrics: dict[str, float]) -> None:
        """Record the run's final result: one stdout line plus results/metrics.json."""
        self.log(metrics)
        RESULTS_DIR.mkdir(parents=True, exist_ok=True)
        path = RESULTS_DIR / "metrics.json"
        path.write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")
        print(f"summary: {json.dumps(metrics)}", flush=True)
        log.info("Saved metrics -> %s", path.relative_to(PROJECT_ROOT))


@contextmanager
def start_run(name: str, params: dict[str, Any]) -> Iterator[Run]:
    """Open a tracked run named by orx's environment, falling back to ``name``."""
    try:
        import trackio
    except ImportError:
        trackio = None

    if trackio is not None:
        trackio.init(
            project=os.environ.get("TRACKIO_PROJECT", name),
            name=os.environ.get("ORX_RUN_ID"),
            group=os.environ.get("ORX_EXPERIMENT"),
            config={
                "hypothesis": os.environ.get("ORX_EXPERIMENT_TITLE"),
                "parent": os.environ.get("ORX_PARENT_EXPERIMENT"),
                "commit": os.environ.get("ORX_COMMIT"),
                **params,
            },
        )
    try:
        yield Run(trackio)
    finally:
        if trackio is not None:
            trackio.finish()
