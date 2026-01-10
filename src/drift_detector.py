import requests
import json
import os
import random

# CONFIGURATION
# In a real app, use os.getenv('GITHUB_TOKEN')
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN") 
REPO_OWNER = "Alez22"     
REPO_NAME = "ProfessionAI_MLOps"            
THRESHOLD = 0.85

def check_model_performance():
    """
    Simulates calculating model accuracy on recent data.
    """
    print("--- Starting Drift Detection ---")
    
    # Simulating a drop in performance (Randomly or fixed for demo)
    # Let's force a low score to demonstrate the trigger
    current_accuracy = 0.75 
    
    print(f"Defined Threshold: {THRESHOLD}")
    print(f"Current Accuracy: {current_accuracy}")

    if current_accuracy < THRESHOLD:
        print("ALARM: Performance drift detected!")
        trigger_retraining(current_accuracy)
    else:
        print("STATUS: Model is performing within limits.")

def trigger_retraining(accuracy):
    """
    Calls GitHub API to trigger the Action.
    """
    if not GITHUB_TOKEN:
        print("ERROR: No GITHUB_TOKEN found. Cannot trigger workflow.")
        return

    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/dispatches"
    
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    payload = {
        "event_type": "model_performance_alert",
        "client_payload": {
            "accuracy": str(accuracy),
            "message": "Drift detected by monitoring system"
        }
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        if response.status_code == 204:
            print("SUCCESS: Retraining workflow triggered via GitHub API.")
        else:
            print(f"FAILED: GitHub API returned {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"ERROR: Could not connect to GitHub. {e}")

if __name__ == "__main__":
    check_model_performance()