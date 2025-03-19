from fastapi import FastAPI
import uuid
from fastapi.middleware.cors import CORSMiddleware
from db import get_db
from tinydb import Query
from request_model import UserRequest
import requests
import os
import getpass
import spacy
from rapidfuzz import process, fuzz

origins = [
    "http://localhost",
    "http://localhost:4200",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

nlp = spacy.load("en_core_web_md")

def find_best_matches_for_eligibility(input_text):
    input_doc = nlp(input_text.lower())
    if input_doc is "all" or input_doc is "any":
        return None
    DB = get_db()
    grants = DB.all()
    choices = set([grant["eligibility"] for grant in grants])
    # Use SpaCy similarity
    similarity_scores = {(choice, input_doc.similarity(nlp(choice.lower()))) for choice in choices if input_doc.similarity(nlp(choice.lower())) > 0.8}
    print(similarity_scores)
    # Use Fuzzy Matching
    choicesUsingFuzzy = process.extract(input_text, choices, scorer=fuzz.partial_ratio, limit=5)
    print(choicesUsingFuzzy)
    return similarity_scores
    
def fetch_grant_details(grant_id):
    # Mock data – Replace this with actual API/database call
    grants = {
        "101": ("Education Grant", "Funding for innovative education projects", "Must have a detailed project plan and budget."),
        "102": ("Healthcare Grant", "Support for community healthcare initiatives", "Must outline expected impact and target beneficiaries.")
    }
    return grants.get(str(grant_id))

   
@app.get("/get-message")
async def test():
    '''
    No args get api call to test if fastapi is working
    '''
    return { "message": "Congrats! The app is running!" }


def generate_grant_application(grant_id, user_details):
    grant = fetch_grant_details(grant_id)
    if not grant:
        return "Grant Not Found"

    title, description, requirements = grant

    prompt = f"""
    You are a grant application expert. Create a complete and professional grant application form for the following grant.
    The application should be well-structured with clear sections and formatting.

    GRANT INFORMATION:
    Title: {title}
    Description: {description}
    Requirements: {requirements}

    APPLICANT INFORMATION:
    Name: {user_details.get('name', '')}
    Organization: {user_details.get('org_name', '')}
    Project Name: {user_details.get('project_name', '')}
    Purpose: {user_details.get('grant_purpose', '')}
    Expected Outcomes: {user_details.get('expected_outcomes', '')}
    Target Audience: {user_details.get('target_audience', '')}
    Contact: {user_details.get('contact_details', '')}

    Generate a complete application form with the following sections:
    1. Executive Summary
    2. Project Description
    3. Objectives and Goals
    4. Implementation Plan
    5. Budget Breakdown
    6. Timeline
    7. Evaluation Metrics
    8. Impact Assessment
    9. Compliance Statement
    10. References

    Format the application as a professional document. Include placeholders for any missing information.
    """

    API_KEY = os.getenv("TOGETHER_API_KEY")
    if not API_KEY:
        API_KEY = getpass.getpass("Enter your Together AI API key: ")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
        "prompt": prompt,
        "max_tokens": 2048,
        "temperature": 0.7,
        "top_p": 0.9
    }

    response = requests.post(
        "https://api.together.xyz/v1/completions",
        headers=headers,
        json=data
    )

    if response.status_code == 200:
        return response.json()["choices"][0]["text"]
    else:
        return f"Error: {response.status_code}, {response.text}"


user_details = {
    "name": "John Doe",
    "org_name": "Education First",
    "project_name": "Tech in Education",
    "grant_purpose": "Introducing AI tools in classrooms",
    "expected_outcomes": "Improved learning efficiency by 20%",
    "target_audience": "High school students",
    "contact_details": "john.doe@example.com"
}

@app.get("/show/{file_id}")
async def file_data(file_id: str):
    '''
    Check the status of the file processing.
    '''
    DB = get_db()
    rows = DB.search(Query().id == file_id)
    if len(rows) > 0:
        status = rows[0]['status']
        if status == "complete":
            return ""
        else:
            return { "status" : status }
    else:
        return {"status": "not found"}


@app.post("/user/input")
async def get_list(request: UserRequest):
    '''
    Input:
    request: contains the question, response and the keyword
    Output:
    returns: headers and output similar to csv for the requested input
    '''
    if request.question == None or request.question == '':
        return { "status": "failure", "response": "Question required" }
    if request.expected == None or request.expected == '':
        return { "status": "failure", "response": "Expected Response required" }
    if request.keyword == None or request.keyword == '':
        return { "status": "failure", "response": "Keyword required for Assertion 2" }
    #assert_row(request.question, request.expected, request.keyword)
    return ""

@app.post("/grants")
async def get_list(request: UserRequest):
    '''
    Input:
    request: contains the category, eligibility, and the location
    Output:
    returns: list of grants for the requested input
    '''
    if request.category == None or len(request.category) == 0:
        return { "status": "failure", "response": "Category required" }
    if request.eligibility == None or len(request.eligibility) == 0:
        return { "status": "failure", "response": "Eligibility required" }
    if request.location == None or request.location == '':
        return { "status": "failure", "response": "Location required" }
    DB = get_db()
    return DB.all()


