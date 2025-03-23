import requests

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
    An effective grant application clearly defines your nonprofit’s needs, leverages storytelling to convey your impact, and specifies realistic goals for the funding you’re requesting.
    You craft a need statement that (1) aligns with the grant-making agency’s funding opportunity announcement; (2) communicates your organization’s experience with restoration projects; and (3) includes several concise – but compelling – anecdotes illustrating the need for restoration.
    """

    API_KEY = os.getenv("TOGETHER_API_KEY")
    if not API_KEY:
        print('API Key not found. Please enter your Together AI API key:')

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