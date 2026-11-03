# AGENTS.md

Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.

---

## Project Context (Agent Research Kit)

This repo is a research project template. Key conventions to respect:

- **Package**: reusable code lives in `src/ark/` (`config`, `seed`, `logging`, `data`, `tracking`). Import via `from ark import ...`.
- **One entry point**: `uv run python main.py` runs the experiment named by `experiment:` in `config.yaml` (a module in `experiments/` exposing `run(params)`), with the hyperparameters under `params:`.
- **Reproducibility**: start every experiment with `set_seed(config.seed)`. Never hard-code paths — use `ark.config` (resolves from repo root). Never hard-code settings — read them from `config.yaml`. Commit `uv.lock`; add dependencies with `uv add <pkg>`.
- **Metrics**: wrap a run in `with start_run(name, params) as tracker:`, call `tracker.log({...}, step=...)` during training and `tracker.summary({...})` once at the end. The summary prints one `summary: {...}` line and writes `results/metrics.json`.
- **Outputs**: figures/tables go to `results/` (git-ignored). **Data** goes under `data/{raw,processed,external}/` (contents git-ignored).
- **Paper**: `paper/main.tex` pulls figures from `results/figures/`.
- **Quality gate**: `uv run ruff check .`, `uv run ruff format --check .` and `uv run pytest` must pass before committing.

## Working in OpenResearch (`orx`)

When this repo is an OpenResearch project, orx adds its own `orx-*` skills to each session; load `orx skill experiment-tree` before driving experiments. The rules that matter for this template:

- **The run command is fixed** for every experiment node: `uv run python main.py`. Never change it per node, pass CLI flags, or vary behaviour through environment variables.
- **Vary code and `config.yaml`, not the command.** To test a hypothesis, create a child node (`orx create-experiment ... --parent <id>`), edit `config.yaml` or the code on the child's branch, commit, then `orx exp run <id>`.
- **Never edit a node after a run has answered it**; branch a child instead.
- **Commit before launching.** Runs use the committed snapshot; uncommitted files are not included.
- Keep tracking through `ark.start_run`, which already reads `TRACKIO_PROJECT` and the `ORX_*` variables orx sets, so `orx metrics <runId>` can find the run. Install Trackio with `uv sync --extra tracking` (or `uv add trackio`).
- Reports and other deliverables go in the session's artifacts directory (`orx-reports`); a paper draft is a `.tex` in the working tree (`orx-paper`).
