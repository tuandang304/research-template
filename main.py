"""Project entry point — the one command every experiment runs.

OpenResearch gives every experiment node the same fixed run command, so this
file stays the same and each node changes only the code and ``config.yaml`` on
its branch. Set the project's run command once to ``uv run python main.py``.

Usage:
    uv run python main.py          # run the experiment named in config.yaml
    uv run python main.py info     # print project info
"""

from __future__ import annotations

import importlib
import sys

# Make `import ark` work when running this file directly, without an install.
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent / "src"))

from ark import __version__, config, get_logger  # noqa: E402

log = get_logger("main")


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    command = argv[0] if argv else "run"

    if command == "info":
        log.info("agent-research-kit v%s", __version__)
        log.info("seed=%d  log_level=%s", config.seed, config.log_level)
        log.info("experiment=%s  params=%s", config.experiment, config.params)
    elif command == "run":
        module = importlib.import_module(f"experiments.{config.experiment}")
        module.run(config.params)
    else:
        log.error("Unknown command: %s (try 'run' or 'info')", command)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
