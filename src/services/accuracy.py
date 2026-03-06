from typing import List, Dict

def compute_accuracy_metrics(y_true: List[int], y_pred: List[int]) -> Dict[str, float]:
    """Return accuracy, precision, recall, f1 and confusion counts for binary labels (1 positive).

    Safe-guards against zero-division are included.
    """
    tp = tn = fp = fn = 0
    for t, p in zip(y_true, y_pred):
        if t == 1 and p == 1:
            tp += 1
        elif t == 0 and p == 1:
            fp += 1
        elif t == 0 and p == 0:
            tn += 1
        elif t == 1 and p == 0:
            fn += 1

    total = tp + tn + fp + fn or 1
    accuracy = (tp + tn) / total
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "tp": tp,
        "tn": tn,
        "fp": fp,
        "fn": fn,
    }
from typing import List, Dict
from datetime import datetime
from src.utils.logging_config import get_logger

logger = get_logger(__name__)


def compute_accuracy(predictions: List[int], ground_truth: List[int]) -> float:
    if not predictions or not ground_truth:
        raise ValueError('Empty predictions or ground_truth')
    if len(predictions) != len(ground_truth):
        raise ValueError('Predictions and ground_truth length mismatch')
    correct = sum(1 for p, g in zip(predictions, ground_truth) if p == g)
    return correct / len(ground_truth)


def compute_accuracy_and_store(predictions: List[int], ground_truth: List[int], meta: Dict = None, db=None) -> Dict:
    meta = meta or {}
    acc = compute_accuracy(predictions, ground_truth)
    record = {
        'accuracy': acc,
        'n': len(ground_truth),
        'meta': meta,
        'timestamp': datetime.utcnow()
    }
    try:
        if db is not None:
            db.accuracy_metrics.insert_one(record)
    except Exception:
        logger.exception('Failed to store accuracy record')
    return {'accuracy': acc, 'n': len(ground_truth)}
