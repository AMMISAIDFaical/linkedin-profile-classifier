import time
import os
import pandas as pd
from dotenv import load_dotenv
from typing import Literal
from pydantic import BaseModel, Field
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from retrivers.third_party_bright_data import get_details

load_dotenv(override=True)

model = ChatOpenAI(
    model=os.getenv("GITHUB_MODEL", "gpt-4.1-mini"),
    base_url="https://models.inference.ai.azure.com",
    api_key=os.environ["GITHUB_TOKEN"]
)

# === Load dataset ===
df = pd.read_csv("/workspaces/linkedin-profile-classifier/app/src/data/TestData.csv")

# === Define tool ===
@tool
def get_profile_details_by_name(url: str):
    """
    Given a person's LinkedIn URL, this tool returns only the most relevant fields:
    name, location, country, about, current company, and up to 3 past experiences (company names only).
    Missing fields are returned as None.
    """
    raw = get_details(url)

    if not raw or not isinstance(raw, dict):
        return {
            "name": None,
            "location": None,
            "country_code": None,
            "about": None,
            "current_company": None,
            "recent_experiences": None,
            "url": url,  # keep the input URL for traceability
        }

    cleaned = {
        "name": (
            raw.get("name")
            or f"{raw.get('first_name', '')} {raw.get('last_name', '')}".strip()
            or None
        ),
        "location": raw.get("location") or raw.get("city") or None,
        "country_code": raw.get("country_code") or None,
        "about": raw.get("about") or None,
        "recent_experiences": (
            [
                exp.get("company") or None
                for exp in (raw.get("experience") or [])[:3]
                if isinstance(exp, dict)
            ]
            or None
        ),
        "url": raw.get("url") or raw.get("input_url") or url,
    }

    return cleaned

# === Define output structure ===
class ProfileType(BaseModel):
    profile_type: Literal["Exited Entrepreneur","Serial Business Angel","Top Mentor","Big Tech C-level","Board Member / Private Investor","Ex-Consulting"] = Field(description="The profile type of the person"),
    reasoning: str = Field(description="The reasoning behind the classification")

# === Prompt ===
prompt = """You are Expert in Vc Firms. 
Your only task is to classify giving collaborators into one of the following categories:
Exited Entrepreneur, Serial Business Angel, Top Mentor, Big Tech C-level, Board Member / Private Investor, Ex-Consulting
Use the tool 'get_profile_details_by_name'Only once to get profile details and then determine the appropriate categories."""

# === Create agent ===
agent = create_agent(
    model=model,
    tools=[get_profile_details_by_name],
    system_prompt=prompt,
    response_format=ProfileType,
    debug=True
)


# === Loop through each row ===
for idx, row in df.iterrows():
    url = row["LinkedIn URL"]
    name = row["First Name"]
    print(f"\nProcessing {name}...")
    time.sleep(10)
    result = agent.invoke({
        "messages": [{"role": "user", "content": str(url)}]
    })
    time.sleep(10)

    structured = result.get("structured_response") if isinstance(result, dict) else None

    if structured:
        df.at[idx, "Profile Type"] = structured.profile_type
        df.at[idx, "Reasoning"] = structured.reasoning
        print(f"{name} → {structured.profile_type}")
    else:
        pass

    
# === Save results ===
df.to_csv("/workspaces/linkedin-profile-classifier/TestData-Classified.csv", index=False)
print("\n Classification complete. Saved to 'Test Data-Classified.csv'.")