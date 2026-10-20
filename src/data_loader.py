"""Load the official AfriSenti Kinyarwanda TSV splits."""
from pathlib import Path
import pandas as pd

BASE_URL = "https://raw.githubusercontent.com/afrisenti-semeval/afrisent-semeval-2023/main/data/kin"

SPLITS = {
    "train": f"{BASE_URL}/train.tsv",
    "validation": f"{BASE_URL}/dev.tsv",
    "test": f"{BASE_URL}/test.tsv",
}


def load_split(split: str) -> pd.DataFrame:
    if split not in SPLITS:
        raise ValueError(f"Unknown split: {split}. Choose from {list(SPLITS)}")
    df = pd.read_csv(SPLITS[split], sep="\t")
    required = {"tweet", "label"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing expected columns: {sorted(missing)}")
    return df[["tweet", "label"]].copy()


def save_raw_splits(output_dir: str = "data/raw") -> None:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    for split in SPLITS:
        df = load_split(split)
        filename = "dev.tsv" if split == "validation" else f"{split}.tsv"
        df.to_csv(out / filename, sep="\t", index=False)


if __name__ == "__main__":
    save_raw_splits()
    print("Saved AfriSenti Kinyarwanda splits to data/raw/")
