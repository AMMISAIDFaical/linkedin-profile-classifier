import os
import time
from pathlib import Path
from datetime import datetime
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
from selenium import webdriver

# CONFIGURATION
INPUT_CSV = "/workspaces/linkedin-profile-classifier/Test Data.csv"
OUTPUT_DIR = Path("scrapes") / f"linkedin_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_CSV = OUTPUT_DIR / "profiles_enriched.csv"

load_dotenv(override=True)

LINKEDIN_EMAIL = os.getenv("LINKEDIN_EMAIL")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")

chrome_opts = Options()
chrome_opts.add_argument("--start-maximized")
chrome_opts.add_argument("--headless=new")  # optional for silent scraping

driver = webdriver.Chrome(options=chrome_opts)
wait = WebDriverWait(driver, 15)

def login():
    """Login to LinkedIn once using env vars."""
    if not LINKEDIN_EMAIL or not LINKEDIN_PASSWORD:
        raise RuntimeError("Please set LINKEDIN_EMAIL and LINKEDIN_PASSWORD environment variables.")
    driver.get("https://www.linkedin.com/login")
    wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(LINKEDIN_EMAIL)
    driver.find_element(By.ID, "password").send_keys(LINKEDIN_PASSWORD)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    wait.until(EC.presence_of_element_located((By.ID, "global-nav-search")))

def get_profile_basic(soup):
    """Extract profile name + headline."""
    name = None
    headline = None
    top_card = soup.find("div", class_="mt2")
    if top_card:
        name_el = top_card.find("h1")
        if name_el: name = name_el.get_text(strip=True)
        headline_el = top_card.find("div", class_="text-body-medium")
        if headline_el: headline = headline_el.get_text(strip=True)
    return {"name": name, "headline": headline}

def get_experience_details():
    """Navigate to /details/experience/ and extract experience list."""
    details_url = driver.current_url.rstrip("/") + "/details/experience/"
    driver.get(details_url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    experiences = []
    for li in soup.find_all("li"):
        title = li.find("span", {"aria-hidden": True})
        title = title.get_text(strip=True) if title else None
        desc_el = li.find("p")
        desc = desc_el.get_text(" ", strip=True) if desc_el else None
        experiences.append({
            "role": title,
            "description": desc
        })
    return experiences

def scrape_profile(profile_url: str):
    """Scrape one profile and return dict."""
    driver.get(profile_url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    basic = get_profile_basic(soup)
    experiences = get_experience_details()

    data = {
        "profile_url": profile_url,
        "name": basic["name"],
        "headline": basic["headline"],
        "experiences": experiences
    }
    return data

login()

test_data = pd.read_csv(INPUT_CSV)
test_data["profile details"] = None

for i, row in test_data.iterrows():
    profile_url = str(row.get("LinkedIn URL", "")).strip()  # adjust column name if different
    print(f"Scraping [{i+1}/{len(test_data)}]: {profile_url}")
    try:
        profile_data = scrape_profile(profile_url)
        # store JSON string of details
        test_data.at[i, "profile details"] = str(profile_data)
        time.sleep(3)
    except Exception as e:
        print(f"[WARN] Failed to scrape {profile_url}: {e}")
        test_data.at[i, "profile details"] = f"Error: {e}"

# ==========================================================
# SAVE OUTPUT
# ==========================================================
test_data.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
print(f"\n All done! Enriched CSV saved at:\n{OUTPUT_CSV}")

driver.quit()
