from fastapi.testclient import TestClient
from src.main import app

# Create a test client for the FastAPI app
client = TestClient(app)

def test_root():
    """Test the root endpoint health check."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "active", "service": "Sentiment Analysis API"}

def test_prediction_positive():
    """Test a positive sentiment prediction."""
    response = client.post("/predict", json={"text": "I love this service!"})
    assert response.status_code == 200
    data = response.json()
    assert data["sentiment"] == "positive"
    assert data["confidence"] > 0.5

def test_prediction_negative():
    """Test a negative sentiment prediction."""
    response = client.post("/predict", json={"text": "This is a disaster."})
    assert response.status_code == 200
    data = response.json()
    assert data["sentiment"] == "negative"

def test_empty_input():
    """Test error handling for empty input."""
    response = client.post("/predict", json={"text": ""})
    assert response.status_code == 400