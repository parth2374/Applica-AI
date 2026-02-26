from crewai import Task
from agents.job_analyzer import job_analyzer
from agents.resume_agent import resume_agent_ats, resume_agent_minimal, resume_agent_recruiter
from agents.cover_letter_agent import cover_letter_agent
from agents.messaging_agent import messaging_agent
from agents.judge_agent import judge_agent

def create_tasks(job_description, user_profile):
    analyze_task = Task(
        description=f"""
        Analyze the following job description and extract:
        - Required skills
        - Tools
        - Experience level

        Job Description:
        {job_description}
        """,
        expected_output="A structured list of required skills, tools, and experience level.",
        agent=job_analyzer
    )

    # Uncomment this block of this

    # resume_task = Task(
    #     description=f"""
    #     Using the extracted job requirements and the candidate profile below,
    #     generate an ATS-optimized resume tailored to the job.

    #     Candidate Profile:
    #     {user_profile}
    #     """,
    #     expected_output="A complete ATS-friendly resume tailored to the job.",
    #     agent=resume_agent,
    #     context=[analyze_task]
    # )

    # Delete from here

    resume_prompt = f"""
    Using the extracted job requirements and the candidate profile below,
    create a tailored resume.

    Candidate Profile:
    {user_profile}
    """

    resume_task_ats = Task(
        description=resume_prompt,
        expected_output="ATS-optimized resume",
        agent=resume_agent_ats,
        context=[analyze_task]
    )

    resume_task_recruiter = Task(
        description=resume_prompt,
        expected_output="Recruiter-friendly resume",
        agent=resume_agent_recruiter,
        context=[analyze_task]
    )

    resume_task_minimal = Task(
        description=resume_prompt,
        expected_output="Minimal clean resume",
        agent=resume_agent_minimal,
        context=[analyze_task]
    )

    judge_task = Task(
        description="""
        You are given multiple resumes for the same job.

        Evaluate them based on:
        - ATS compatibility
        - Relevance to job
        - Clarity and impact

        Select the BEST resume.
        Explain why it was chosen.
        Provide the final improved resume.
        """,
        expected_output="Best resume with justification",
        agent=judge_agent,
        context=[
            resume_task_ats,
            resume_task_recruiter,
            resume_task_minimal
        ]
    )

    # Delete till here

    cover_letter_task = Task(
        description=f"""
        Write a personalized cover letter for this job using the resume
        and job requirements.
        """,
        expected_output="A professional, personalized cover letter.",
        agent=cover_letter_agent,
        # context=[resume_task]
        context=[judge_task]
    )

    messaging_task = Task(
        description="""
        Write a short LinkedIn or email outreach message to a recruiter
        regarding this job application.
        """,
        expected_output="A concise recruiter outreach message.",
        agent=messaging_agent,
        context=[cover_letter_task]
    )

    # return [analyze_task, resume_task, cover_letter_task, messaging_task]
    return [
        analyze_task,
        resume_task_ats,
        resume_task_recruiter,
        resume_task_minimal,
        judge_task,
        cover_letter_task,
        messaging_task
    ]