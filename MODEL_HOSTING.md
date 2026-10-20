# Upload the trained model for deployment

The trained checkpoint is large, so don't commit it directly to a normal GitHub repository. The simplest deploy arrangement is to keep code on GitHub and the model checkpoint in a separate Hugging Face model repository.

## Before starting

- Confirm the local project contains `models/afroxlmr_lr1e5_best/`.
- Create/sign in to your Hugging Face account.
- Create a **write** access token on Hugging Face and keep it private. Do not paste it into source code, chat, README, or GitHub.
- If you use the uploader script below, install the upload dependency: `python -m pip install -U huggingface_hub`.

## Upload with the script

From the project root after copying `scripts/upload_model_to_hub.py` into the `scripts/` folder, run:

```bash
python scripts/upload_model_to_hub.py --repo-id YOUR_HF_USERNAME/kinyarwanda-afroxlmr-sentiment --public
```

When prompted, sign in using the Hugging Face CLI (`hf auth login`) with your token first. The script uploads only the selected folder `models/afroxlmr_lr1e5_best/`, not the other experiment checkpoints.

**`--public` means the uploaded model files will be publicly downloadable.** Check the pretrained model license and your course/data rules before publishing. If you don't want the model public, omit `--public`; a private repo needs a securely configured token in the deployed app, so deployment setup is a little more involved.

After upload, open the model page and confirm it contains `config.json`, tokenizer files, and `model.safetensors` (or the saved model weight file).

## Configure Streamlit Community Cloud

In the app's settings under Secrets, add:

```toml
MODEL_REPO_ID = "YOUR_HF_USERNAME/kinyarwanda-afroxlmr-sentiment"
```

No Hugging Face token is required at inference time if the model repository is public. The model download can take a few minutes the first time.
