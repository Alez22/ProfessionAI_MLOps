from fastapi.testclient import TestClient
from src.main import app
import pytest

# Initialize the TestClient with our FastAPI app
# This creates a "fake" web browser that can send requests to the app directly in memory
client = TestClient(app)

def test_health_check():
    """
    Verifies that the API is up and running.
    Goal: Check if the /health endpoint returns 200 OK.
    """
    response = client.get("/health")
    
    # Assertions: If these fail, the pipeline stops (Red X)
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert "model" in response.json()

def test_predict_positive_sentiment():
    """
    Verifies the model correctly identifies positive sentiment.
    """
    payload = {"text": "MachineInnovators creates amazing technology!"}
    response = client.post("/predict", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    
    # We expect 'positive' label
    assert data["sentiment"] == "positive"
    # Confidence should be reasonably high
    assert data["confidence"] > 0.5

def test_predict_negative_sentiment():
    """
    Verifies the model correctly identifies negative sentiment.
    """
    payload = {"text": "The service is down and support is terrible."}
    response = client.post("/predict", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["sentiment"] == "negative"

def test_empty_input_validation():
    """
    Verifies that the API correctly handles invalid input (empty text).
    Expected: 400 Bad Request
    """
    payload = {"text": ""}
    response = client.post("/predict", json=payload)
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Text cannot be empty"

def test_metrics_endpoint_existence():
    """
    Verifies that Prometheus metrics are exposed.
    This ensures monitoring is configured correctly.
    """
    response = client.get("/metrics")
    assert response.status_code == 200
    # Check if some standard prometheus metric text is present
    assert "http_requests_total" in response.text