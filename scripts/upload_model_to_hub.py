"""Upload only the selected fine-tuned AfroXLM-R checkpoint to Hugging Face Hub."""
import argparse
from pathlib import Path

from huggingface_hub import HfApi


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-id", required=True, help="e.g. username/kinyarwanda-afroxlmr-sentiment")
    parser.add_argument("--model-dir", default="models/afroxlmr_lr1e5_best")
    parser.add_argument("--public", action="store_true", help="Make model repository public (files become downloadable by anyone)")
    args = parser.parse_args()

    model_dir = Path(args.model_dir).expanduser().resolve()
    if not model_dir.is_dir():
        raise SystemExit(f"Model directory not found: {model_dir}")
    if not (model_dir / "config.json").exists():
        raise SystemExit(f"config.json not found in {model_dir}; this does not look like a saved Transformers model folder.")
    if not any((model_dir / filename).exists() for filename in ("model.safetensors", "pytorch_model.bin")):
        # Sharded safetensors models use an index file instead of a single model.safetensors file.
        if not (model_dir / "model.safetensors.index.json").exists():
            raise SystemExit("No model weight file found. Check that the selected checkpoint was saved completely.")

    api = HfApi()
    api.create_repo(repo_id=args.repo_id, repo_type="model", private=not args.public, exist_ok=True)
    api.upload_folder(
        folder_path=str(model_dir),
        repo_id=args.repo_id,
        repo_type="model",
        commit_message="Upload selected fine-tuned AfroXLM-R sentiment checkpoint",
    )
    print(f"Uploaded model to https://huggingface.co/{args.repo_id}")
    if args.public:
        print("The model repository is public. Anyone may download its files.")
    else:
        print("The model repository is private. Configure authenticated access before deploying a public app.")


if __name__ == "__main__":
    main()
