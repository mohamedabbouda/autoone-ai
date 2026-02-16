from __future__ import annotations

from pathlib import Path
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, accuracy_score
from sklearn.linear_model import LogisticRegression


DATA_PATH = Path("data/datasets/reco_training.csv")
MODEL_DIR = Path("models")
MODEL_DIR.mkdir(parents=True, exist_ok=True)


FEATURE_COLS = [
    "f_rating_norm",
    "f_distance_closeness",
    "f_open_now",
    "position",
    "hour",
    "dayofweek",
]


def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_PATH}. Run build_dataset first.")

    df = pd.read_csv(DATA_PATH)

    # Keep only rows with valid labels
    df = df.dropna(subset=["label_clicked"])

    # Basic sanity checks
    if df["label_clicked"].sum() == 0:
        raise RuntimeError(
            "No positive clicks in dataset (label_clicked=1). "
            "Generate at least a few recommend+click events first."
        )

    X = df[FEATURE_COLS].fillna(0.0)
    y = df["label_clicked"].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    model = LogisticRegression(max_iter=200, class_weight="balanced")
    model.fit(X_train, y_train)

    # Evaluate
    proba = model.predict_proba(X_test)[:, 1]
    preds = (proba >= 0.5).astype(int)

    auc = roc_auc_score(y_test, proba)
    acc = accuracy_score(y_test, preds)

    print(f"✅ Trained Logistic Regression ranker")
    print(f"Rows: {len(df)} | Positives: {int(df['label_clicked'].sum())}")
    print(f"AUC: {auc:.3f} | Accuracy: {acc:.3f}")

    # Save model + metadata
    artifact = {
        "model": model,
        "feature_cols": FEATURE_COLS,
    }
    out_path = MODEL_DIR / "reco_lr.pkl"
    joblib.dump(artifact, out_path)
    print(f"✅ Saved model to: {out_path}")


if __name__ == "__main__":
    main()
