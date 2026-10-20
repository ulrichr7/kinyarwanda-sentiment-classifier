# Kinyarwanda Sentiment Classifier

A Streamlit application for three-class Kinyarwanda sentiment classification (negative, neutral, positive), using a fine-tuned AfroXLM-R model.

## Results

The selected configuration (learning rate `1e-5`) achieved **0.6614 validation macro-F1** and **65.01% test accuracy / 0.6498 test macro-F1** on the project evaluation. Neutral sentiment was the hardest class. Seven manually chosen app examples are qualitative checks only and are not a representative accuracy estimate.

## Run locally

1. Use the project's Python environment. For the app only, install `requirements.txt`; to reproduce the notebooks and training experiments, use `requirements-dev.txt`:
   ```bash
   python -m pip install -r requirements-dev.txt
   ```
2. Ensure the fine-tuned model folder exists at `models/afroxlmr_lr1e5_best/`.
3. Run from the project root:
   ```bash
   streamlit run app.py
   ```

## Deploy

Model weights are deliberately excluded from GitHub. GitHub blocks ordinary files larger than 100 MiB; this repository uses a separate Hugging Face model repository for the fine-tuned checkpoint.

1. Upload the contents of `models/afroxlmr_lr1e5_best/` to a Hugging Face **model** repository (see `MODEL_HOSTING.md`).
2. Deploy this GitHub repository with Streamlit Community Cloud, selecting `app.py` as the entrypoint.
3. In Streamlit app settings, add this secret, replacing the example with your Hugging Face model repo ID:
   ```toml
   MODEL_REPO_ID = "YOUR_HF_USERNAME/kinyarwanda-afroxlmr-sentiment"
   ```
4. Restart/redeploy the app. The app will download the model from the public Hub repository when it starts.

A public model repository is the simplest arrangement for a public demo; do not put personal access tokens or other secrets in this README or in source control. If you keep the model repository private, deployment needs secure authentication configured separately.

## Project structure

- `app.py` — interactive Streamlit application
- `src/` — source/data-loading/model code, if included in the working project
- `notebooks/` — exploration and experiments; clear notebook outputs before publishing
- `results/` — aggregate experiment metrics (avoid committing files containing raw tweets)
- `models/` and `data/` — local-only; not committed to GitHub

## Limitations

This is an educational prototype. The held-out test macro-F1 was 0.6498. The hand-selected app examples surfaced errors on negative expressions and negation. Predicted probabilities are not calibrated confidence guarantees. Review dataset/model licensing and avoid publishing user identifiers or raw social-media posts unnecessarily.

## Live demo

Open the deployed application:

https://kinyarwanda-sentiment-classifiergit-bcgzl5tg7g2ncymwarhjks.streamlit.app

The app predicts negative, neutral, or positive sentiment for Kinyarwanda text using the fine-tuned AfroXLM-R model.
