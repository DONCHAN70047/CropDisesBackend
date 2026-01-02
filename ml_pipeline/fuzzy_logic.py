import numpy as np

def fuzzy_scale(predictions):
    """
    Apply fuzzy logic scaling to prediction scores
    Input: predictions -> list of dicts, e.g., [{"class": "Brown Spot", "confidence": 0.95}, ...]
    Output: scaled_predictions -> list of dicts
    """
    scaled_predictions = []
    for pred in predictions:
        confidence = pred["confidence"]
        if confidence > 0.9:
            scaled_conf = min(1.0, confidence + 0.05)
        elif confidence < 0.5:
            scaled_conf = max(0.0, confidence - 0.05)
        else:
            scaled_conf = confidence
        scaled_predictions.append({
            "class": pred["class"],
            "confidence": scaled_conf
        })
    return scaled_predictions
