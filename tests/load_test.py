import requests
import time
import random
import sys

URL = "http://localhost:8000/predict"

def generate_traffic():
    print(f"--- Starting Load Test hitting {URL} ---")
    
    test_data = ["Good service", "Bad error", "Normal day"]

    success_count = 0
    
    for i in range(10): # Riduciamo a 10 per debug
        text = random.choice(test_data)
        try:
            response = requests.post(URL, json={"text": text}, timeout=5)
            
            # --- DEBUG STAMPA ---
            if response.status_code == 200:
                print(f"Req {i+1}: OK ({response.json()['sentiment']})")
                success_count += 1
            else:
                # STAMPIAMO L'ERRORE VERO
                print(f"Req {i+1}: FAILED. Status: {response.status_code}")
                print(f"Body: {response.text}")
                
        except Exception as e:
            print(f"Req {i+1}: CONNECTION ERROR: {e}")
        
        time.sleep(0.5)

    if success_count == 0:
        print("CRITICAL: All requests failed.")
        sys.exit(1) # Fail the pipeline
    else:
        print("--- Load Test Complete ---")

if __name__ == "__main__":
    generate_traffic()