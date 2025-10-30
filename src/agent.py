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
    model=os.getenv("GITHUB_MODEL", "gpt-5"),
    base_url="https://models.inference.ai.azure.com",
    api_key=os.environ["GITHUB_TOKEN"]
)

# === Load dataset ===
df = pd.read_csv("/workspaces/linkedin-profile-classifier/src/data/Test Data.csv").head(1)

# === Define tool ===
@tool
def get_profile_details_by_name(url: str):
    """
    Given a person's url, this tool will return their 'profile details'.
    """
    response = get_details(url)
    return response

# === Define output structure ===
class ProfileType(BaseModel):
    profile_type: Literal["Exited Entrepreneur","Serial Business Angel","Top Mentor","Big Tech C-level","Board Member / Private Investor",
        "Ex-Consulting"] = Field(description="The profile type of the person"),
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
    response_format=ToolStrategy(ProfileType),
    debug=True
)

# === Initialize empty column ===
df["profile type"] = None

# === Loop through each row ===
for idx, row in df.iterrows():
    url = row["LinkedIn URL"]
    name = row["First Name"]
    print(f"\nProcessing {name}...")

    result = agent.invoke({
        "messages": [{"role": "user", "content": str(url)}]
    })

    structured = result.get("structured_response") if isinstance(result, dict) else None

    if structured:
        df.at[idx, "Profile Type"] = structured.profile_type
        print(f"{name} → {structured.profile_type}")
    else:
        pass

    
# === Save results ===
df.to_csv("/workspaces/linkedin-profile-classifier/Test Data - Classified.csv", index=False)
print("\n Classification complete. Saved to 'Test Data - Classified.csv'.")
