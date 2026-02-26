from crewai import Agent, LLM
from langchain_google_genai import ChatGoogleGenerativeAI
import os

llm = LLM(
    model="models/gemini-2.5-flash-lite",
    temperature=0.2,
    provider="google",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

job_analyzer = Agent(
    role="Job Description Analyst",
    goal="Analyze job descriptions and extract required skills, tools, and qualifications",
    backstory=(
        "You are an expert HR analyst who understands job descriptions, "
        "ATS systems, and hiring requirements."
    ),
    llm=llm,
    verbose=True
)