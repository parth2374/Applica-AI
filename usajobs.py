import requests
import os
from dotenv import load_dotenv

load_dotenv()

USAJOBS_API_KEY = os.getenv("USAJOBS_API_KEY")
USAJOBS_EMAIL = os.getenv("USAJOBS_EMAIL")

BASE_URL = "https://data.usajobs.gov/api/search"


def fetch_jobs(keyword, location="", results=5):
    headers = {
        "Authorization-Key": USAJOBS_API_KEY,
        "User-Agent": USAJOBS_EMAIL
    }

    params = {
        "Keyword": keyword,
        "LocationName": location,
        "ResultsPerPage": results
    }

    response = requests.get(BASE_URL, headers=headers, params=params)

    if response.status_code != 200:
        raise Exception(f"USAJobs API Error: {response.status_code}")

    return response.json()