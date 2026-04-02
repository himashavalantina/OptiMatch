import PyPDF2
import requests
import json

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    text = ""
    try:
        with open(pdf_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text()
        return text.lower()
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""

def fetch_jooble_jobs(skills, api_key, location=""):
    """Fetches live jobs from Jooble API using a POST request."""
    url = f"https://jooble.org/api/2d506b3a-2fdb-4f12-a3a4-a47937a0a87d"
    body = {
        "keywords": skills,
        "location": location
    }
    try:
        response = requests.post(url, json=body)
        if response.status_code == 200:
            data = response.json()
            return data.get('jobs', [])
        else:
            print(f"Error: Jooble returned status code {response.status_code}")
            return []
    except Exception as e:
        print(f"Error fetching jobs from Jooble: {e}")
        return []