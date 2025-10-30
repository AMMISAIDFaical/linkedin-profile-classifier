from time import time
import requests
from dotenv import load_dotenv
import os
import json
import time

load_dotenv(override=True)

BRIGHT_DATA_API_KEY = os.getenv("BRIGHT_DATA_API_KEY")

headers = {
    "Authorization": f"Bearer {BRIGHT_DATA_API_KEY}",
    "Content-Type": "application/json",
}

def get_details(url):

    time.sleep(40)

    data = json.dumps({
        "input": [{"url": url}],
    })
    response = requests.post(
        "https://api.brightdata.com/datasets/v3/scrape?dataset_id=gd_l1viktl72bvl7bjuj0&notify=false&include_errors=true",
        headers=headers,
        data=data
    )

    return response.json()

if __name__ == "__main__":
    test_url = "https://linkedin.com/in/benmah"
    result = get_details(test_url)
    print(json.dumps(result, indent=2))