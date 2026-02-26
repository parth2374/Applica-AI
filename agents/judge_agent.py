# Delete this file

from crewai import Agent, LLM
from langchain_google_genai import ChatGoogleGenerativeAI
import os

llm = LLM(
    model="models/gemini-2.5-flash-lite",
    temperature=0.2,
    provider="google",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

judge_agent = Agent(
    role="Resume Judge",
    goal="Evaluate multiple resumes and select the best one for the job",
    backstory=(
        "Senior hiring manager and ATS expert who understands both "
        "machine screening and human evaluation"
    ),
    llm=llm,
    verbose=True
)