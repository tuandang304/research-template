# Research template

A minimal, reproducible Python research project, ready to use as an
[OpenResearch](https://github.com/tuandang304/OpenResearch) project.

## Quickstart

```bash
uv sync                  # install the exact versions in uv.lock
uv run python main.py    # run the experiment named in config.yaml
```

The example trains a classifier, prints a `summary: {...}` line, and writes
`results/metrics.json` and a figure to `results/figures/`.

## With OpenResearch

1. In `orx up`, create a project from this repository's URL.
2. Set the run command once: `uv run python main.py`.
3. Each experiment node changes only `config.yaml` or the code on its branch.
4. For metric charts beside each run: `uv add trackio`.

## Layout

```
config.yaml        seed, which experiment to run, its params
main.py            the fixed entry point
experiments/       one module per experiment, each with run(params)
src/ark/           config, seeding, logging, metric tracking
tests/             smoke tests (uv run pytest)
data/ results/     created at run time, git-ignored
```

Add dependencies with `uv add <package>` and commit `uv.lock`.
