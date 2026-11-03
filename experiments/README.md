# Experiments

Each module here exposes `run(params)`. `main.py` runs the one named by
`experiment:` in `config.yaml`, passing it the `params:` from the same file, so
every run uses the same command:

```bash
uv run python main.py
```

Each run should be **reproducible**: seed everything via `set_seed(config.seed)`,
read every setting from `params`, wrap the run in `start_run(...)`, end with
`tracker.summary({...})`, and write outputs to `results/`.

- `example_experiment.py` — a complete, runnable example (trains a classifier,
  logs its accuracy, saves a confusion-matrix figure).

To try a variant, change `config.yaml` (or the code) and commit it. In
OpenResearch, do that on a child experiment's branch and keep the run command
unchanged.
