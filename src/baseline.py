"""Baseline: TF-IDF word n-grams + Logistic Regression."""
from pathlib import Path
import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, classification_report
from sklearn.pipeline import Pipeline

LABEL_ORDER = ["negative", "neutral", "positive"]


def load_tsv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, sep="\t")
    return df.dropna(subset=["tweet", "label"]).copy()


def train_baseline(train_path="data/raw/train.tsv", test_path="data/raw/test.tsv"):
    train = load_tsv(train_path)
    test = load_tsv(test_path)

    model = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True)),
        ("clf", LogisticRegression(max_iter=2000, class_weight="balanced", random_state=42)),
    ])
    model.fit(train["tweet"], train["label"])
    pred = model.predict(test["tweet"])

    accuracy = accuracy_score(test["label"], pred)
    precision, recall, f1, _ = precision_recall_fscore_support(
        test["label"], pred, average="macro", zero_division=0
    )
    report = classification_report(test["label"], pred, zero_division=0, output_dict=True)
    metrics = {"accuracy": accuracy, "macro_precision": precision, "macro_recall": recall, "macro_f1": f1, "classification_report": report}
    Path("results").mkdir(exist_ok=True)
    Path("results/baseline_metrics.json").write_text(json.dumps(metrics, indent=2))
    return model, metrics


if __name__ == "__main__":
    model, metrics = train_baseline()
    print(json.dumps({k: v for k, v in metrics.items() if k != "classification_report"}, indent=2))
