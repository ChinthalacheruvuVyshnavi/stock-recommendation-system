import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sklearn.metrics import accuracy_score, classification_report
from tqdm import tqdm

print("Loading FinBERT model...")

model_name = "ProsusAI/finbert"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)
model.eval()

print("Model loaded successfully.")

id2label = {
    0: "positive",
    1: "negative",
    2: "neutral"
}

label2id = {
    "positive": 0,
    "negative": 1,
    "neutral": 2
}

file_path = "data/Sentences_50Agree.txt"

texts = []
true_labels = []

print("Loading dataset...")

with open(file_path, "r", encoding="latin-1") as f:
    for line in f:
        sentence, sentiment = line.strip().rsplit("@", 1)
        texts.append(sentence)
        true_labels.append(label2id[sentiment.lower()])

print(f"Total samples loaded: {len(texts)}")

predictions = []

print("Evaluating model...")

for text in tqdm(texts):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=256)

    with torch.no_grad():
        outputs = model(**inputs)

    probs = torch.nn.functional.softmax(outputs.logits, dim=1)
    predicted_class = torch.argmax(probs, dim=1).item()
    predictions.append(predicted_class)

accuracy = accuracy_score(true_labels, predictions)

print("\nFinBERT Accuracy on Financial PhraseBank Dataset:")
print("Accuracy:", round(accuracy * 100, 2), "%")

print("\nClassification Report:")
print(classification_report(true_labels, predictions, target_names=["positive", "negative", "neutral"]))