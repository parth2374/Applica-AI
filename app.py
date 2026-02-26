import streamlit as st
import os
from datetime import datetime

from usajobs import fetch_jobs
from agent_tasks import create_tasks
from crew import create_crew

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(
    page_title="Applica AI",
    page_icon="Logo.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------
# Session State Initialization
# --------------------------------------------------
default_states = {
    "jobs": [],
    "selected_job": None,
    "generated": False,
    "job_analysis": "",
    "resume_ats": "",
    "resume_recruiter": "",
    "resume_minimal": "",
    "final_resume": "",
    "cover_letter": "",
    "message": "",
}

for key, value in default_states.items():
    if key not in st.session_state:
        st.session_state[key] = value

# --------------------------------------------------
# Header
# --------------------------------------------------
st.title("🤖 AI Job Application Assistant")
st.caption(
    "Multi-agent system that analyzes jobs, compares resumes, and generates job-ready applications"
)

# --------------------------------------------------
# Sidebar — Job Search
# --------------------------------------------------
with st.sidebar:
    st.header("🔍 Job Search")

    keyword = st.text_input("Job Keyword", placeholder="Python Developer")
    location = st.text_input("Location", placeholder="Remote / New York")

    if st.button("Search Jobs", use_container_width=True):
        with st.spinner("Fetching jobs from USAJobs..."):
            data = fetch_jobs(keyword, location)
            st.session_state.jobs = data["SearchResult"]["SearchResultItems"]
            st.session_state.generated = False

# --------------------------------------------------
# Main Layout
# --------------------------------------------------
left, right = st.columns([1, 2])

# --------------------------------------------------
# Job Selection
# --------------------------------------------------
with left:
    st.subheader("📌 Available Jobs")

    if st.session_state.jobs:
        job_titles = [
            f"{i+1}. {j['MatchedObjectDescriptor']['PositionTitle']}"
            for i, j in enumerate(st.session_state.jobs)
        ]

        selected_index = st.selectbox(
            "Select a job",
            range(len(job_titles)),
            format_func=lambda x: job_titles[x],
        )

        job = st.session_state.jobs[selected_index]["MatchedObjectDescriptor"]
        st.session_state.selected_job = job

        st.success("Job selected")

# --------------------------------------------------
# Job Description
# --------------------------------------------------
with right:
    st.subheader("📝 Job Description")

    if st.session_state.selected_job:
        job_description = st.session_state.selected_job.get(
            "QualificationSummary", "No description available."
        )
        st.write(job_description)
    else:
        job_description = ""
        st.info("Select a job to view its description")

# --------------------------------------------------
# User Profile
# --------------------------------------------------
st.divider()
st.subheader("👤 Your Profile")

user_profile = st.text_area(
    "Paste your resume / skills / experience",
    height=220,
    placeholder=(
        "Example:\n"
        "Python developer with 2+ years experience.\n"
        "Worked with FastAPI, SQL, automation, REST APIs, data analysis..."
    ),
)

# --------------------------------------------------
# Generate Application
# --------------------------------------------------
if st.button("🚀 Generate Application", type="primary"):

    if not st.session_state.selected_job or not user_profile.strip():
        st.warning("Please select a job and enter your profile.")
    else:
        with st.spinner("Running AI agents (analysis → comparison → generation)..."):
            tasks = create_tasks(job_description, user_profile)
            crew = create_crew(tasks)
            result = crew.kickoff()

            outputs = result.tasks_output

            # --- Task Outputs (ORDER MATTERS) ---
            st.session_state.job_analysis = outputs[0].raw

            st.session_state.resume_ats = outputs[1].raw
            st.session_state.resume_recruiter = outputs[2].raw
            st.session_state.resume_minimal = outputs[3].raw

            # Judge output = final resume + reasoning
            st.session_state.final_resume = outputs[4].raw

            st.session_state.cover_letter = outputs[5].raw
            st.session_state.message = outputs[6].raw

            st.session_state.generated = True

        # --------------------------------------------------
        # Save Outputs
        # --------------------------------------------------
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        os.makedirs("outputs", exist_ok=True)

        with open(f"outputs/application_{timestamp}.txt", "w", encoding="utf-8") as f:
            f.write("=== JOB ANALYSIS ===\n")
            f.write(st.session_state.job_analysis + "\n\n")

            f.write("=== ATS RESUME ===\n")
            f.write(st.session_state.resume_ats + "\n\n")

            f.write("=== RECRUITER RESUME ===\n")
            f.write(st.session_state.resume_recruiter + "\n\n")

            f.write("=== MINIMAL RESUME ===\n")
            f.write(st.session_state.resume_minimal + "\n\n")

            f.write("=== FINAL SELECTED RESUME (JUDGE) ===\n")
            f.write(st.session_state.final_resume + "\n\n")

            f.write("=== COVER LETTER ===\n")
            f.write(st.session_state.cover_letter + "\n\n")

            f.write("=== RECRUITER MESSAGE ===\n")
            f.write(st.session_state.message)

        st.success("Application generated successfully 🎉")

# --------------------------------------------------
# Output Section
# --------------------------------------------------
if st.session_state.generated:
    st.divider()
    st.header("📄 Generated Application")

    tabs = st.tabs(
        [
            "🔍 Job Analysis",
            "🧠 Resume Comparison",
            "🏆 Final Resume",
            "✉️ Cover Letter",
            "💬 Recruiter Message",
        ]
    )

    with tabs[0]:
        st.markdown(st.session_state.job_analysis)

    with tabs[1]:
        st.subheader("ATS Optimized Resume")
        st.markdown(st.session_state.resume_ats)
        st.divider()

        st.subheader("Recruiter Friendly Resume")
        st.markdown(st.session_state.resume_recruiter)
        st.divider()

        st.subheader("Minimal Resume")
        st.markdown(st.session_state.resume_minimal)

    with tabs[2]:
        st.markdown(st.session_state.final_resume)
        st.download_button(
            "⬇️ Download Final Resume",
            st.session_state.final_resume,
            file_name="final_resume.txt",
            use_container_width=True,
        )

    with tabs[3]:
        st.markdown(st.session_state.cover_letter)
        st.download_button(
            "⬇️ Download Cover Letter",
            st.session_state.cover_letter,
            file_name="cover_letter.txt",
            use_container_width=True,
        )

    with tabs[4]:
        st.markdown(st.session_state.message)
        st.download_button(
            "⬇️ Download Recruiter Message",
            st.session_state.message,
            file_name="recruiter_message.txt",
            use_container_width=True,
        )

    st.caption("⬆️ Downloads do not regenerate content. All outputs saved locally.")