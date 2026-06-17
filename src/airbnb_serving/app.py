import os
from contextlib import asynccontextmanager

import mlflow
import mlflow.sklearn
from fastapi import FastAPI, Request

from airbnb_serving.predictor import predict_batch, predict_single
from airbnb_serving.schema import ListingFeatures, PredictionResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    tracking_uri = os.environ.get("MLFLOW_TRACKING_URI")
    run_id = os.environ.get("MODEL_RUN_ID")

    missing = [
        name
        for name in (
            "MLFLOW_TRACKING_URI",
            "MLFLOW_TRACKING_USERNAME",
            "MLFLOW_TRACKING_PASSWORD",
            "MODEL_RUN_ID",
        )
        if not os.environ.get(name)
    ]
    if missing:
        raise RuntimeError(f"Missing required environment variables: {', '.join(missing)}")

    mlflow.set_tracking_uri(tracking_uri)
    app.state.model = mlflow.sklearn.load_model(f"runs:/{run_id}/model")
    app.state.model_run_id = run_id
    yield


app = FastAPI(title="Airbnb Demand Serving", version="0.1.0", lifespan=lifespan)


@app.get("/health")
def health(request: Request) -> dict[str, str]:
    return {"status": "ok", "model_run_id": request.app.state.model_run_id}


@app.post("/predict", response_model=PredictionResponse)
def predict(features: ListingFeatures, request: Request) -> PredictionResponse:
    return predict_single(features, request.app.state.model, request.app.state.model_run_id)


@app.post("/predict/batch", response_model=list[PredictionResponse])
def predict_batch_endpoint(
    features_list: list[ListingFeatures], request: Request
) -> list[PredictionResponse]:
    return predict_batch(features_list, request.app.state.model, request.app.state.model_run_id)
