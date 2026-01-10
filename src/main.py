from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.model import SentimentAnalyzer
from prometheus_fastapi_instrumentator import Instrumentator
import sys

app = FastAPI(title="MachineInnovators Reputation Monitor")

# --- GLOBAL VARIABLES ---
analyzer = None       # Variabile per il modello
startup_error = None  # Variabile per catturare l'errore se qualcosa esplode

# --- MODEL LOADING ---
print("--- ATTEMPTING TO LOAD MODEL ---")
try:
    analyzer = SentimentAnalyzer()
    print("--- MODEL LOADED SUCCESSFULLY ---")
except Exception as e:
    # Catturiamo l'errore esatto!
    startup_error = str(e)
    print(f"--- CRITICAL STARTUP ERROR: {startup_error} ---")
    # Non facciamo crashare l'app qui, altrimenti Docker si riavvia all'infinito 
    # e non riusciamo a leggere l'errore.
    pass

# Setup Prometheus
Instrumentator().instrument(app).expose(app)

# --- MODELS ---
class SentimentRequest(BaseModel):
    text: str

class SentimentResponse(BaseModel):
    sentiment: str
    confidence: float

# --- ENDPOINTS ---
@app.get("/")
def read_root():
    return {"status": "active"}

@app.get("/health")
def health_check():
    # Se c'è stato un errore all'avvio, lo diciamo subito
    if startup_error:
        raise HTTPException(status_code=500, detail=f"Startup Failed: {startup_error}")
    if not analyzer:
        raise HTTPException(status_code=503, detail="Model loading...")
    return {"status": "ok", "model": analyzer.MODEL_NAME}

@app.post("/predict", response_model=SentimentResponse)
def predict(request: SentimentRequest):
    # CONTROLLO CRITICO DI DEBUG
    global analyzer, startup_error
    
    # 1. Se il modello non è caricato perché c'è stato un errore all'avvio:
    if analyzer is None:
        error_msg = startup_error if startup_error else "Unknown initialization error"
        # RESTITUIAMO L'ERRORE VERO AL CLIENT
        raise HTTPException(status_code=500, detail=f"MODEL LOAD FAILED: {error_msg}")

    if not request.text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    try:
        label, score = analyzer.predict(request.text)
        return {"sentiment": label, "confidence": score}
    except Exception as e:
        print(f"Inference Error: {e}")
        raise HTTPException(status_code=500, detail=f"Inference Error: {str(e)}")