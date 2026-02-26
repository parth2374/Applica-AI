from crewai import Agent, LLM
from langchain_google_genai import ChatGoogleGenerativeAI
import os

llm = LLM(
    model="models/gemini-2.5-flash-lite",
    temperature=0.2,
    provider="google",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

cover_letter_agent = Agent(
    role="Cover Letter Writer",
    goal="Write personalized and compelling cover letters",
    backstory="Career coach who writes engaging cover letters",
    llm=llm,
    verbose=True
)