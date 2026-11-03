<div align="center">

# 🔬 Agent Research Kit

**A reproducible, AI-agent-ready template for academic & data-science research.**

Clone it, run one command, and start doing research — with a clean project
structure, reproducibility built in, a LaTeX paper scaffold, and
[Claude Code](https://claude.com/claude-code) skills pre-installed.

[![CI](https://github.com/tuandang304/research-template/actions/workflows/ci.yml/badge.svg)](https://github.com/tuandang304/research-template/actions/workflows/ci.yml)
[![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code style: ruff](https://img.shields.io/badge/style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Use this template](https://img.shields.io/badge/use%20this-template-2ea44f?logo=github)](https://github.com/tuandang304/research-template/generate)

[English](README.md) · [Tiếng Việt](README.vi.md)

</div>

---

## Why this template?

Most research code starts as a messy notebook and never recovers. This template
gives you a **professional scaffold on day one** so your work stays reproducible,
shareable, and easy to turn into a paper.

- 🧪 **Reproducible by default** — one place for config, one call to seed every RNG.
- 📁 **Sensible structure** — `data/ · notebooks/ · experiments/ · results/ · paper/`.
- 📦 **Ready to run** — `uv sync` installs everything; a real example experiment ships in the box.
- 📄 **Paper-ready** — LaTeX scaffold that pulls figures straight from `results/`, plus a `CITATION.cff`.
- 🤖 **AI-agent-ready** — bundled Claude Code skills for API work, citations, system design, and more.
- ✅ **Batteries included** — tests, linting (ruff), CI, and issue/PR templates already wired up.

## Quickstart

> Requires [**uv**](https://docs.astral.sh/uv/) (recommended) or plain `pip`.

```bash
# 1. Get the code (or click "Use this template" on GitHub)
git clone https://github.com/tuandang304/research-template.git
cd research-template

# 2. Install everything into an isolated environment
uv sync                     # pinned by uv.lock; dev tools included. --extra notebook for Jupyter

# 3. Run the experiment in config.yaml — trains a model, prints a summary line,
#    and writes results/metrics.json and a figure to results/figures/
uv run python main.py
```

Prefer pip? `python -m venv .venv && source .venv/bin/activate && pip install -e ".[notebook]" ruff pytest`

That's it — you now have a working, reproducible research project.

## Use it with OpenResearch

The template is built to be an [OpenResearch](https://github.com/tuandang304/OpenResearch)
project out of the box:

1. In `orx up`, create a project and paste this repository's URL as the repository to
   clone (or `git clone` it yourself and import the folder).
2. Set the run command once: `orx project edit <projectId> --run-command 'uv run python main.py'`.
3. Create the baseline node and run it. Every child node keeps that command and
   changes only `config.yaml` or the code on its own branch.
4. For metric charts beside each run, `uv add trackio` (or `uv sync --extra tracking`).
   `ark.start_run` already uses the `ORX_*` and `TRACKIO_PROJECT` variables orx sets,
   so `orx metrics <runId>` finds the run. Without Trackio, the `summary:` line in the
   run log and `results/metrics.json` still carry the result.

Agents read [AGENTS.md](AGENTS.md) (Claude Code reads it through `CLAUDE.md`).

## Project structure

```
research-template/
├── src/ark/                # Your reusable package (config, seeding, logging, data IO, tracking)
├── experiments/            # Experiment modules, each exposing run(params)
├── notebooks/              # Exploration; 01_exploratory.ipynb is wired to `ark`
├── data/                   # raw / processed / external  (contents git-ignored)
├── results/                # figures / tables            (regenerated, git-ignored)
├── paper/                  # LaTeX scaffold + references.bib → uses results/figures
├── docs/                   # Design notes, data docs, experiment log
├── tests/                  # pytest smoke tests
├── config.yaml             # The one config: seed, experiment to run, its params
├── main.py                 # The fixed run command:  uv run python main.py [info]
├── AGENTS.md · CLAUDE.md   # Instructions for coding agents
├── .claude/ · .agents/     # Pre-installed Claude Code skills (see below)
├── pyproject.toml          # Metadata, dependencies, ruff & pytest config
└── uv.lock                 # Exact dependency versions — commit it
```

## Reproducibility conventions

Every experiment follows the same rules, so results are trivial to reproduce:

```python
from ark import config, set_seed, start_run


def run(params):
    set_seed(config.seed)  # 1. Seed Python, NumPy, and PyTorch (if installed)
    with start_run("my_exp", params) as tracker:  # 2. Track metrics (Trackio if installed)
        ...  # 3. Read settings from params (config.yaml) — never hard-code
        tracker.summary({"accuracy": 0.93})  # 4. One final summary line + results/metrics.json
```

Point `experiment:` in `config.yaml` at your module, and `uv run python main.py` runs it.
Dependencies are pinned in `uv.lock`; add new ones with `uv add <package>`.

Paths resolve from the repo root via `ark.config`, so the same code works from a
script, a notebook, or a test — no `../../` guesswork.

## From experiment to paper

Figures written to `results/figures/` are picked up directly by `paper/main.tex`
(`\graphicspath{{../results/figures/}}`). Build the paper with `latexmk -pdf main.tex`
or drop the folder into [Overleaf](https://overleaf.com). GitHub will also show a
**"Cite this repository"** button thanks to `CITATION.cff`.

## Bundled Claude Code skills 🤖

If you use [Claude Code](https://claude.com/claude-code), these skills load
automatically from `.claude/skills/` (mirrored in `.agents/skills/`):

| Skill | Helps you… |
| --- | --- |
| **claude-api** | Build with the Claude API across 8 languages (caching, tools, batches). |
| **bibtex-citation** | Fetch and format correct BibTeX entries for `paper/references.bib`. |
| **system-design** | Draft architecture and design docs for `docs/`. |
| **skill-creator / skill-development** | Author your own project skills. |
| **agent-development / plugin-structure** | Build custom agents and plugins. |
| **memory-management** | Give agents durable project memory. |

Not using Claude Code? These folders are inert — delete them and nothing breaks.

## Customize it

After clicking **Use this template**, make it yours:

1. Rename the package `src/ark/` → `src/<your_project>` and update `pyproject.toml`.
2. Fill in author fields in `pyproject.toml`, `LICENSE`, and `CITATION.cff`.
3. Add your dependencies with `uv add <package>` (updates `uv.lock`).
4. Delete the example experiment and `paper/`/`.claude/` bits you don't need.

## Contributing

Issues and PRs are welcome — see [CONTRIBUTING.md](CONTRIBUTING.md). If this
template saves you time, a ⭐ helps others find it!

## License

[MIT](LICENSE) — free for academic and commercial use.
