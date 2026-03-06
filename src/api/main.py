from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

from src.services.distance_calculator import calculate_engine_distance
from src.services.live_api import fetch_live_train_info
from src.services.accuracy import compute_accuracy_and_store
from src.db.mongo import get_db
from src.utils.logging_config import get_logger

logger = get_logger(__name__)

app = FastAPI(title="Railway Coach Analytics API")


class DistanceRequest(BaseModel):
    engine: dict
    coaches: List[dict]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/distance")
def engine_distance(req: DistanceRequest):
    try:
        dist = calculate_engine_distance(req.engine, req.coaches)
        return {"distance_m": dist}
    except Exception as e:
        logger.exception("Distance calculation failed")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/live/{train_no}")
def live_info(train_no: str, db=Depends(get_db)):
    try:
        info = fetch_live_train_info(train_no)
        return info
    except Exception as e:
        logger.exception("Live API fetch failed")
        raise HTTPException(status_code=502, detail=str(e))


class AccuracyPayload(BaseModel):
    predictions: List[int]
    ground_truth: List[int]
    meta: Optional[dict] = None


@app.post("/accuracy")
def accuracy(payload: AccuracyPayload, db=Depends(get_db)):
    try:
        result = compute_accuracy_and_store(payload.predictions, payload.ground_truth, payload.meta, db)
        return result
    except Exception as e:
        logger.exception("Accuracy computation failed")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=8000, reload=True)
