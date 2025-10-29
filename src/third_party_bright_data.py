import requests
import json
import pandas as pd
from dotenv import load_dotenv
load_dotenv(override=True)

BRIGHT_DATA_API_KEY = os.getenv("BRIGHT_DATA_API_KEY")

headers = {
    "Authorization": BRIGHT_DATA_API_KEY,
    "Content-Type": "application/json",
}

test_data = pd.read_csv("/Users/faicalammisaid/Documents/projects/inovexus/linkedin-profile-classifier/Test Data.csv")

test_data["profile details"] = None

for i, row in test_data.iterrows():
    url = row["LinkedIn URL"]

    data = {
        "input": [{"url": url}]
    }

    response = requests.post(
        "https://api.brightdata.com/datasets/v3/scrape?dataset_id=gd_l1viktl72bvl7bjuj0&notify=false&include_errors=true",
        headers=headers,
        json=data
    )

    test_data.at[i, "profile details"] = response.text

test_data.to_csv("/Users/faicalammisaid/Documents/projects/inovexus/linkedin-profile-classifier/Test Data - Enriched.csv", index=False)

