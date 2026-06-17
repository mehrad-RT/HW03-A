FROM python:3.11-slim AS builder

WORKDIR /build
COPY requirements.txt pyproject.toml ./
COPY src/ ./src/
RUN pip install --no-cache-dir --target=/install -r requirements.txt && \
    pip install --no-cache-dir --target=/install .

FROM python:3.11-slim

WORKDIR /app
ENV PYTHONPATH=/install
COPY --from=builder /install /install
COPY src/ ./src/
COPY pyproject.toml requirements.txt ./

EXPOSE 8000
CMD ["python", "-m", "uvicorn", "airbnb_serving.app:app", "--host", "0.0.0.0", "--port", "8000"]
