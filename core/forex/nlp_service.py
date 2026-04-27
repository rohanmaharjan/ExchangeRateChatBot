from transformers import pipeline

# zero-shot classification model
classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"
)

LABELS = [
    "compare currencies",
    "latest exchange rate",
    "highest buy rate",
    "lowest buy rate",
    "currency trend",
    "rate change analysis"
]


def detect_intent_nlp(user_input):
    result = classifier(
        user_input,
        candidate_labels=LABELS
    )

    return result["labels"][0]