from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.model import SentimentAnalyzer
from prometheus_fastapi_instrumentator import Instrumentator

# Initialize the application
app = FastAPI(title="MachineInnovators Reputation Monitor")

# Initialize the model (Global variable to load it only once)
analyzer = SentimentAnalyzer()

# Enable Prometheus monitoring
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
    """Health check endpoint."""
    return {"status": "active", "service": "Sentiment Analysis API"}

@app.post("/predict", response_model=SentimentResponse)
def predict(request: SentimentRequest):
    """
    Receives text and returns sentiment classification.
    """
    if not request.text:
        raise HTTPException(status_code=400, detail="Input text cannot be empty.")

    try:
        label, score = analyzer.predict(request.text)
        return {"sentiment": label, "confidence": score}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))