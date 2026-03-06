from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.utils.haversine import distance_km
from src.services.accuracy import compute_accuracy_metrics
from src.utils.logging_config import get_logger

logger = get_logger("engine_distance_api")

app = FastAPI(title="Railway Coach Analytics API")


class DistanceRequest(BaseModel):
    lat1: float
    lon1: float
    lat2: float
    lon2: float


class AccuracyRequest(BaseModel):
    y_true: list
    y_pred: list


@app.post("/distance")
def calc_distance(req: DistanceRequest):
    try:
        km = distance_km(req.lat1, req.lon1, req.lat2, req.lon2)
        return {"distance_km": km}
    except Exception as e:
        logger.exception("Distance calculation error: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/accuracy")
def calc_accuracy(req: AccuracyRequest):
    try:
        metrics = compute_accuracy_metrics(req.y_true, req.y_pred)
        return metrics
    except Exception as e:
        logger.exception("Accuracy calculation error: %s", e)
        raise HTTPException(status_code=500, detail=str(e))
