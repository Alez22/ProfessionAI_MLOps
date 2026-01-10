# 🚀 MachineInnovators Reputation Monitor (MLOps)

Welcome to the **Reputation Monitoring System**, an end-to-end MLOps project designed to analyze social media sentiment using state-of-the-art AI models. This repository demonstrates a **Level 4 MLOps Maturity** pipeline, featuring automated testing, continuous integration, drift detection, automated retraining triggers, and cloud deployment.

---

## 🏗️ Architecture Overview

The system is built using a microservices architecture orchestrated by **Docker**.

| Component | Technology | Description |
|:---|:---|:---|
| **Model** | Hugging Face (RoBERTa) | `twitter-roberta-base-sentiment-latest` for SOTA sentiment analysis |
| **Serving** | FastAPI | High-performance REST API for real-time inference |
| **Containerization** | Docker | Ensures reproducibility across environments |
| **CI/CD** | GitHub Actions | Automates Build, Test, and Deploy workflows |
| **Monitoring** | Prometheus & Grafana | Real-time metrics collection (Latency, Throughput) |
| **Drift Detection** | Python Script | Checks model accuracy and triggers retraining if performance drops |
| **Deployment** | Hugging Face Spaces | Docker-based deployment for public access |

---

## 🛠️ Project Structure

```
reputation-monitoring/
├── .github/
│   └── workflows/          # CI/CD Pipelines (Build, Test, Deploy, Retrain)
├── monitoring/             # Configuration for Prometheus & Grafana
├── src/                    # Source Code
│   ├── main.py            # FastAPI Application Entry Point
│   ├── model.py           # AI Model Logic (RoBERTa Wrapper)
│   └── drift_detector.py  # Script for performance monitoring
├── tests/                  # Integration & Load Tests
├── Dockerfile              # Blueprint for the application container
├── docker-compose.yml      # Orchestration of API + Monitoring Stack
└── requirements.txt        # Python Dependencies
```

---

## 🚦 CI/CD Pipeline Logic

Every time code is pushed to the `main` branch, the MLOps End-to-End Pipeline executes the following steps:

1. **Build & Setup**: Builds the Docker containers and installs dependencies (fixing PyTorch CPU versions to save space)
2. **Start Services**: Launches the full stack (API, Prometheus, Grafana) using Docker Compose
3. **Integration Testing**: Runs `pytest` to verify API health and inference logic
4. **Load Testing**: Simulates real traffic (`tests/load_test.py`) to generate live metrics in Prometheus
5. **Drift Detection**: The `drift_detector.py` script analyzes performance. If accuracy < 0.80, it triggers the Automated Retraining Workflow via GitHub API
6. **Deployment (CD)**: If all tests pass, the application is automatically deployed to Hugging Face Spaces

---

## 🖥️ How to Run Locally

You can run the entire system on your machine using Docker.

### Prerequisites

- Docker & Docker Compose installed

### Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   cd reputation-monitoring
   ```

2. **Start the Stack**:
   ```bash
   docker compose up --build
   ```

3. **Access the Services**:
   - **API (Swagger UI)**: http://localhost:8000/docs
   - **Grafana Dashboard**: http://localhost:3000 (User: `admin`, Pass: `admin`)
   - **Prometheus**: http://localhost:9090

---

## 🛡️ Project Design Choices

### Why RoBERTa instead of FastText?

While the project prompt mentioned FastText, the specific requirement linked to the `cardiffnlp/twitter-roberta-base-sentiment-latest` model. We chose RoBERTa (a Transformer model) because it significantly outperforms FastText on social media text by understanding context, sarcasm, and slang.

### Why GitHub Actions for Retraining?

Instead of using heavy orchestrators like Airflow (which consume excessive resources for a single pipeline), we implemented an **Event-Driven Architecture**. The monitoring script uses the GitHub API to trigger a `repository_dispatch` event, launching a dedicated GitHub Action workflow for retraining. This "Serverless MLOps" approach saves resources and is cost-effective.

---

## 👩‍💻 Credits

Project developed for the **ProfessionAI MLOps Course**.