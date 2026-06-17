
# Airbnb Demand Prediction — Model Serving Service

A **FastAPI** service that loads a trained **scikit-learn** model from **MLflow** and exposes a REST API for predicting high-demand Airbnb listings.

## What this does

- Loads a pre-trained Random Forest pipeline from MLflow **once** at startup
- Exposes three endpoints:
  - `GET /health` — service health check
  - `POST /predict` — predict for a single listing
  - `POST /predict/batch` — predict for multiple listings in one request
- Packaged in Docker with a size-optimized multi-stage build
- Ready for Kubernetes deployment with proper manifests

## Quick start (local)

```bash
# 1. Create virtual environment and install
python3 -m venv .venv
source .venv/bin/activate
pip install -e .

# 2. Set required environment variables
export MLFLOW_TRACKING_URI=<your_mlflow_URL>
export MLFLOW_TRACKING_USERNAME=<your_mlflow_username>
export MLFLOW_TRACKING_PASSWORD=<your_mlflow_password>
export MODEL_RUN_ID=<your_model_run_id>

# 3. Start the server
uvicorn airbnb_serving.app:app --host 0.0.0.0 --port 8000

# 4. Test it
curl http://localhost:8000/health
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"instant_bookable": true, "accommodates": 2, ...}'
```

## Docker

```bash
# Build the optimized image
docker build -t qbc12-airbnb-serving:optimized .

# Run with docker-compose
echo "MLFLOW_TRACKING_URI=..." > .env
echo "MLFLOW_TRACKING_USERNAME=..." >> .env
echo "MLFLOW_TRACKING_PASSWORD=..." >> .env
echo "MODEL_RUN_ID=..." >> .env
docker compose up -d
```

## Requirements

- Python ≥ 3.11
- FastAPI, Uvicorn, MLflow, scikit-learn, Pandas, Pydantic v2
- See `pyproject.toml` for exact versions
