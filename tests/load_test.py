import requests
import time
import random
import sys

# API Endpoint (running in Docker container)
URL = "http://localhost:8000/predict"

def generate_traffic():
    """
    Sends random requests to the API to generate Prometheus metrics.
    """
    print("--- Starting Load Test to populate Metrics ---")
    
    test_data = [
        "MachineInnovators is the best!",
        "I hate this service, it is terrible.",
        "Just a normal day at the office.",
        "Support is very helpful.",
        "App crashes all the time."
    ]

    # Send 20 requests to generate some history
    for i in range(20):
        text = random.choice(test_data)
        try:
            response = requests.post(URL, json={"text": text})
            if response.status_code == 200:
                print(f"Request {i+1}: {response.json()['sentiment']}")
            else:
                print(f"Request {i+1}: Failed")
        except Exception as e:
            print(f"Connection Error: {e}")
            sys.exit(1)
        
        # Small sleep to simulate real traffic time
        time.sleep(0.1)

    print("--- Load Test Complete. Metrics updated in Prometheus. ---")

if __name__ == "__main__":
    generate_traffic()