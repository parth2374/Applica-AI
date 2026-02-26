from crewai import Agent, LLM
from langchain_google_genai import ChatGoogleGenerativeAI
import os

llm = LLM(
    model="models/gemini-2.5-flash-lite",
    temperature=0.2,
    provider="google",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

messaging_agent = Agent(
    role="Outreach Specialist",
    goal="Write professional LinkedIn and email outreach messages",
    backstory="Recruiter communication expert",
    llm=llm,
    verbose=True
)