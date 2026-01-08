# src/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.model import SentimentAnalyzer
from prometheus_fastapi_instrumentator import Instrumentator

# 1. Initialize the Application
app = FastAPI(title="MachineInnovators Reputation Monitor")

# 2. Load the AI Model
# We initialize it here so it loads once when the container starts.
# This might take a few seconds to download/load the weights.
try:
    analyzer = SentimentAnalyzer()
except Exception as e:
    print(f"Failed to load model: {e}")
    # We don't exit here to allow the app to start, 
    # but the health check will reveal the issue.

# 3. Setup Prometheus Monitoring
# This automatically exposes the /metrics endpoint for Grafana
Instrumentator().instrument(app).expose(app)

# --- Data Models (Pydantic) ---

class SentimentRequest(BaseModel):
    text: str

class SentimentResponse(BaseModel):
    sentiment: str
    confidence: float

# --- Endpoints ---

@app.get("/")
def read_root():
    """
    Root endpoint to verify the service is running.
    """
    return {"status": "active", "service": "Sentiment Analysis API"}

@app.get("/health")
def health_check():
    """
    Health check endpoint for Docker and Kubernetes.
    Checks if the model is loaded and ready.
    """
    if not analyzer:
        raise HTTPException(status_code=503, detail="Model not loaded yet")
    return {"status": "ok", "model": analyzer.MODEL_NAME}

@app.post("/predict", response_model=SentimentResponse)
def predict(request: SentimentRequest):
    """
    Main inference endpoint.
    Receives text -> Returns sentiment (Positive/Neutral/Negative).
    """
    if not request.text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    try:
        # Perform inference using the pre-loaded model
        label, score = analyzer.predict(request.text)
        return {"sentiment": label, "confidence": score}
    except Exception as e:
        # Log the error (in a real app) and return 500
        print(f"Inference Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Model Error")