from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

MODEL_NAME = "ProsusAI/finbert"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
model.eval()

# FinBERT mapping
ID2LABEL = {
    0: "positive",
    1: "negative",
    2: "neutral"
}


def finbert_sentiment(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=256)

    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=1)

    predicted_idx = torch.argmax(probs, dim=1).item()
    confidence = float(probs[0][predicted_idx].item())

    return {
        "label": ID2LABEL[predicted_idx],
        "confidence": round(confidence * 100, 2)
    }


def finbert_sentiment_batch(texts):
    results = []
    for text in texts:
        results.append(finbert_sentiment(text))
    return results