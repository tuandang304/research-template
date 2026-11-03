# Contributing

Thanks for your interest in improving **Agent Research Kit**! 🎉

## Ways to contribute

- **Report bugs / request features** via [Issues](https://github.com/tuandang304/research-template/issues).
- **Improve docs** — typos, clarifications, and better examples are always welcome.
- **Submit code** via pull request (see below).

## Development setup

```bash
git clone https://github.com/tuandang304/research-template.git
cd research-template
uv sync                    # dev tools come from the `dev` dependency group
uv run pre-commit install  # optional: format & lint on commit
```

## Before opening a PR

```bash
uv run ruff format .       # format
uv run ruff check . --fix  # lint
uv run pytest              # tests must pass
```

Keep changes focused and match the existing style. For anything non-trivial,
open an issue first so we can align on the approach.

## Code of conduct

Be respectful and constructive. We want this to be a welcoming project for
researchers and students of all levels.
