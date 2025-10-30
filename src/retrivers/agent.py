import os
import ast
import pandas as pd
from dotenv import load_dotenv
from typing import Literal
from pydantic import BaseModel, Field
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

# === Setup ===
load_dotenv(override=True)

API_HOST = os.getenv("API_HOST", "github")
model = ChatOpenAI(
    model=os.getenv("GITHUB_MODEL", "gpt-4o"),
    base_url="https://models.inference.ai.azure.com",
    api_key=os.environ["GITHUB_TOKEN"]
)

# === Load your dataset ===
df = pd.read_csv("/workspaces/linkedin-profile-classifier/Test Data - Enriched.csv")

# === Prompt instructions ===
prompt = """You are an expert talent analyst. Your task is to classify a LinkedIn profile into one or more of the following categories:
1. Exited Entrepreneur : founded a company that was acquired, merged, or exited.
2. Serial Business Angel : invests in multiple startups personally (not via fund).
3. Top Mentor : mentors founders or startups through accelerators or programs.
4. Big Tech C-level : executive (CEO, CTO, CIO, VP, Director).
5. Board Member / Private Investor : serves on company boards or invests via private equity / venture capital.
6. Ex-Consulting : formerly worked at McKinsey, BCG, Bain, or similar top consulting firms.
Use the provided profile details to determine the appropriate categories. If none apply, respond with 'None'."""

# === Define tool ===
@tool
def get_profile_details_by_name(person_name: str) -> str:
    """Given a person's name, return their 'profile details' from the enriched CSV."""
    match = df[df["First Name"].str.lower() == person_name.strip().lower()]
    if match.empty:
        print(f"No profile found for name: {person_name}")
        return None

    profile_data = match.iloc[0]["profile details"]
    try:
        profile_data = ast.literal_eval(profile_data)
    except (ValueError, SyntaxError):
        pass
    return profile_data

# === Define structured output ===
class ProfileType(BaseModel):
    profile_type: Literal[
        "Exited Entrepreneur",
        "Serial Business Angel",
        "Top Mentor",
        "Big Tech C-level",
        "Board Member / Private Investor",
        "Ex-Consulting",
        "None"
    ] = Field(description="The profile type of the person")

# === Create agent ===
agent = create_agent(
    model=model,
    tools=[get_profile_details_by_name],
    response_format=ProfileType
)

# === Apply the agent to each row ===
def classify_profile(row):
    try:
        name = row["First Name"]
        # Call the agent for each profile
        result = agent.invoke({
            "messages": [
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"Classify {name} based on their profile details."}
            ]
        })
        structured = result.get("structured_response", None)
        return structured.profile_type if structured else "None"
    except Exception as e:
        print(f"Error processing {row['First Name']}: {e}")
        return "Error"

# Run classification on each row
df["profile type"] = df.apply(classify_profile, axis=1)

# === Save the result ===
df.to_csv("/workspaces/linkedin-profile-classifier/Test-Data-Classified.csv", index=False)
print("Classification complete. Results saved to 'Test Data - Classified.csv'.")
