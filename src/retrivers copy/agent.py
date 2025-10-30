import os
import ast
import pandas as pd
from dotenv import load_dotenv
from typing import Literal
from pydantic import BaseModel, Field
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from typing import Sequence
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from typing_extensions import Annotated, TypedDict

from retrivers.retrivers.third_party_bright_data import get_details
# === Setup ===
load_dotenv(override=True)

model = ChatOpenAI(
    model=os.getenv("GITHUB_MODEL", "gpt-4o"),
    base_url="https://models.inference.ai.azure.com",
    api_key=os.environ["GITHUB_TOKEN"]
)

# === Load dataset ===
df = pd.read_csv("/workspaces/linkedin-profile-classifier/Test Data - Enriched.csv")

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
    profile_type: Literal[
        "Exited Entrepreneur",
        "Serial Business Angel",
        "Top Mentor",
        "Big Tech C-level",
        "Board Member / Private Investor",
        "Ex-Consulting",
        "None"
    ] = Field(description="The profile type of the person")

# === Prompt ===
prompt = """You are a helpful assistant. Your task is to classify inovexus collaborators into one of the following categories:
1. Exited Entrepreneur : founded a company.
2. Serial Business Angel : invests in startups personally (not via fund).
3. Top Mentor : mentors founders or startups.
4. Big Tech C-level : executive (CEO, CTO, CIO, VP, Director).
5. Board Member / Private Investor : serves on company boards or invests via private equity / venture capital.
6. Ex-Consulting : formerly worked at top consulting firms.
Use the tool 'get_profile_details_by_name'  Only once ! to get profile details and then determine the appropriate categories."""

# === Create agent ===
agent = create_agent(
    model=model,
    tools=[get_profile_details_by_name],
    system_prompt=prompt,
    response_format=ProfileType
)

# === Initialize empty column ===
df["profile type"] = None

# === Loop through each row ===
for idx, row in df.iterrows():
    agent = create_agent(
        model=model,
        tools=[get_profile_details_by_name],
        system_prompt=prompt,
        response_format=ProfileType
    )

    url = row["LinkedIn URL"]
    name = row["First Name"]
    print(f"\n Processing {name}...")

    result = agent.invoke({
    "messages": [{"role": "user", "content": name + '' + url}]
    })

    result["structured_response"]

    
# === Save results ===
df.to_csv("/workspaces/linkedin-profile-classifier/Test Data - Classified.csv", index=False)
print("\n Classification complete. Saved to 'Test Data - Classified.csv'.")
