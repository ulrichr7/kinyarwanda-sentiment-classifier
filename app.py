"""Streamlit demo for the fine-tuned Kinyarwanda sentiment classifier."""
from pathlib import Path
import os

import pandas as pd
import streamlit as st
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

ROOT = Path(__file__).resolve().parent
LOCAL_MODEL_DIR = ROOT / "models" / "afroxlmr_lr1e5_best"
LABELS = ["negative", "neutral", "positive"]
MAX_LENGTH = 128

st.set_page_config(
    page_title="Kinyarwanda Sentiment Classifier",
    page_icon="💬",
    layout="centered",
)


def configured_model_id() -> str:
    """Read optional Hugging Face model repo ID from environment or Streamlit secrets."""
    model_id = os.getenv("MODEL_REPO_ID", "").strip()
    if model_id:
        return model_id
    try:
        model_id = str(st.secrets.get("MODEL_REPO_ID", "")).strip()
    except Exception:
        model_id = ""
    return model_id


def choose_model_source() -> str:
    """Use local trained weights during local development, otherwise Hub repo ID."""
    if (LOCAL_MODEL_DIR / "config.json").exists():
        return str(LOCAL_MODEL_DIR)
    model_id = configured_model_id()
    if model_id:
        return model_id
    raise FileNotFoundError(
        "The fine-tuned model was not found locally and MODEL_REPO_ID is not set. "
        "Upload models/afroxlmr_lr1e5_best to a Hugging Face model repository, "
        "then set MODEL_REPO_ID in the deployment settings."
    )


@st.cache_resource(show_spinner="Loading the trained AfroXLM-R model…")
def load_model(model_source: str):
    device = torch.device(
        "mps" if torch.backends.mps.is_available() else "cpu"
    )
    tokenizer = AutoTokenizer.from_pretrained(model_source)
    model = AutoModelForSequenceClassification.from_pretrained(model_source)
    model.to(device)
    model.eval()
    return tokenizer, model, device


def predict_sentiment(text: str, tokenizer, model, device):
    encoded = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=MAX_LENGTH,
    )
    encoded = {key: value.to(device) for key, value in encoded.items()}
    with torch.inference_mode():
        logits = model(**encoded).logits
        probabilities = torch.softmax(logits, dim=-1)[0].cpu().tolist()

    predicted_id = max(range(len(probabilities)), key=probabilities.__getitem__)
    config_labels = getattr(model.config, "id2label", {}) or {}
    raw_label = config_labels.get(predicted_id, config_labels.get(str(predicted_id), LABELS[predicted_id]))
    predicted_label = str(raw_label).lower()
    if predicted_label not in LABELS:
        predicted_label = LABELS[predicted_id]

    probs = {LABELS[i].capitalize(): float(probabilities[i]) for i in range(len(LABELS))}
    return predicted_label, probs


st.title("Kinyarwanda Sentiment Classifier")
st.write(
    "Enter a Kinyarwanda social-media message to predict whether its expressed "
    "sentiment is negative, neutral, or positive."
)
st.caption(
    "Fine-tuned AfroXLM-R · Maximum input length: 128 tokens · "
    "Predictions can be wrong, particularly for ambiguous or mixed sentiment."
)

try:
    model_source = choose_model_source()
    tokenizer, model, device = load_model(model_source)
except Exception as exc:
    st.error(
        "The trained model could not be loaded. Locally, check that "
        "models/afroxlmr_lr1e5_best exists. In deployment, check the "
        "MODEL_REPO_ID setting and that the model repository is accessible. "
        f"Details: {type(exc).__name__}: {exc}"
    )
    st.stop()

st.caption(f"Inference device: `{device}`")

with st.form("sentiment_form"):
    message = st.text_area(
        "Kinyarwanda text",
        height=150,
        placeholder="Andika ubutumwa bwawe mu Kinyarwanda hano…",
        help="Paste one message. Inputs longer than 128 tokens are truncated.",
    )
    submitted = st.form_submit_button("Analyze sentiment", type="primary")

if submitted:
    text = message.strip()
    if not text:
        st.warning("Please enter a message before running the prediction.")
    else:
        with st.spinner("Analyzing sentiment…"):
            prediction, probabilities = predict_sentiment(text, tokenizer, model, device)
        title = prediction.capitalize()
        st.subheader("Prediction")
        st.metric("Predicted sentiment", title)
        st.write(f"Model probability for this class: **{probabilities[title]:.1%}**")
        st.subheader("Class probabilities")
        st.bar_chart(pd.DataFrame({"Probability": probabilities}))
        st.caption(
            "Probabilities are model outputs, not calibrated guarantees of correctness. "
            "Avoid using an individual prediction for consequential decisions."
        )

with st.expander("About this project"):
    st.markdown(
        "- **Task:** three-class Kinyarwanda sentiment classification.\n"
        "- **Dataset:** AfriSenti Kinyarwanda subset; duplicate overlaps were checked.\n"
        "- **Selected model:** fine-tuned AfroXLM-R (`Davlan/afro-xlmr-base`).\n"
        "- **Model selection:** validation macro-F1.\n"
        "- **Known limitation:** neutral sentiment was the hardest class on the held-out test set."
    )
