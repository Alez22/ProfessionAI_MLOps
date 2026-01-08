# ProfessionAI_MLOps
Project for MLOps course.

## Development & Testing ✅

- To run unit tests quickly without downloading the heavy transformer model, set the environment variable `USE_FAKE_MODEL=1`. The repository includes a lightweight `FakeSentimentAnalyzer` in `src/fakes.py` used by tests to avoid external downloads.

- Fast test (uses fake model):

```
USE_FAKE_MODEL=1 pytest
```

- Full test with the real model (will download weights and require `torch`/`transformers`):

```
pip install -r requirements.txt
pytest
```

- The CI workflow is configured to use `requirements-test.txt` and sets `USE_FAKE_MODEL=1` for fast, deterministic tests.

## Scheduled Retraining ⏱️

- A scheduled GitHub Actions workflow (`.github/workflows/scheduled_retrain.yml`) runs `scripts/retrain.py` daily (02:00 UTC) and uploads any retrained model artifacts as workflow artifacts. The job installs minimal training deps (scikit-learn + joblib) and uses the simple backend by default.

- You can run the retrainer locally with:

```
python scripts/retrain.py --model-path models/sentiment/model.joblib --threshold 0.7 --output-dir models/sentiment
```

- The retrain orchestrator will evaluate current model performance and trigger a retrain with the simple backend when accuracy falls below the threshold. For production scheduled training with Hugging Face training, add a separate heavier workflow that installs `requirements-train.txt` and runs `src/train.py --backend hf`.