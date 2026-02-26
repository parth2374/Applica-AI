from crewai import Agent, LLM
from langchain_google_genai import ChatGoogleGenerativeAI
import os

llm = LLM(
    model="models/gemini-2.5-flash-lite",
    temperature=0.2,
    provider="google",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

# Uncomment this

# resume_agent = Agent(
#     role="Resume Writer",
#     goal="Create ATS-friendly resumes tailored to specific job descriptions",
#     backstory="Professional resume writer with ATS optimization expertise",
#     llm=llm,
#     verbose=True
# )

# Delete from here

resume_agent_ats = Agent(
    role="ATS Resume Specialist",
    goal="Create an ATS-optimized resume with maximum keyword matching",
    backstory="Expert in ATS systems, keyword density, parsing rules",
    verbose=True,
    llm=llm
)

resume_agent_recruiter = Agent(
    role="Recruiter-Focused Resume Writer",
    goal="Create a resume that impresses human recruiters",
    backstory="10+ years hiring engineers, values clarity and impact",
    verbose=True,
    llm=llm
)

resume_agent_minimal = Agent(
    role="Minimal Resume Designer",
    goal="Create a concise, clean resume with only high-signal content",
    backstory="Specialist in minimalist professional resumes",
    verbose=True,
    llm=llm
)

# Delete till here