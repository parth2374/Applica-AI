from crewai import Crew
from agents.job_analyzer import job_analyzer
from agents.resume_agent import resume_agent_minimal, resume_agent_ats, resume_agent_recruiter
from agents.cover_letter_agent import cover_letter_agent
from agents.messaging_agent import messaging_agent

def create_crew(tasks):
    return Crew(
        agents=[
            job_analyzer,
            resume_agent_recruiter,
            # Delete from here
            resume_agent_ats,
            resume_agent_minimal,
            cover_letter_agent,
            # Delete till here and apply text which was here earlier
            messaging_agent
        ],
        tasks=tasks,
        verbose=True
    )