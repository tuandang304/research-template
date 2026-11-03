"""A complete, runnable example experiment.

It trains a small classifier on a built-in dataset, logs its metrics, and saves
a confusion-matrix figure to ``results/figures/``. ``main.py`` runs it with the
``params`` from ``config.yaml``; copy it to start a new experiment.

    uv run python main.py
"""

from __future__ import annotations

from typing import Any

from ark import config, get_logger, set_seed, start_run
from ark.config import FIGURES_DIR, PROJECT_ROOT

log = get_logger("experiment")


def run(params: dict[str, Any]) -> None:
    set_seed(config.seed)
    log.info("Running example experiment (seed=%d, params=%s)", config.seed, params)

    # Lazy imports so the package itself stays import-light.
    import matplotlib

    matplotlib.use("Agg")  # headless-safe backend
    import matplotlib.pyplot as plt
    from sklearn import datasets
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import ConfusionMatrixDisplay, accuracy_score
    from sklearn.model_selection import train_test_split

    with start_run("example", params) as tracker:
        X, y = getattr(datasets, f"load_{params['dataset']}")(return_X_y=True)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=params["test_size"], random_state=config.seed, stratify=y
        )

        model = RandomForestClassifier(
            n_estimators=params["n_estimators"], random_state=config.seed
        )
        model.fit(X_train, y_train)

        preds = model.predict(X_test)
        acc = accuracy_score(y_test, preds)
        tracker.summary({"test_accuracy": round(float(acc), 4)})

    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    fig_path = FIGURES_DIR / "example_confusion_matrix.png"
    ConfusionMatrixDisplay.from_predictions(y_test, preds)
    plt.title(f"{params['dataset']} — RandomForest (acc={acc:.2f})")
    plt.tight_layout()
    plt.savefig(fig_path, dpi=150)
    log.info("Saved figure -> %s", fig_path.relative_to(PROJECT_ROOT))


if __name__ == "__main__":
    run(config.params)
