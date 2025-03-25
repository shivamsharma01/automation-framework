from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from request_model import UserRequest, GenerateGrantRequest
from grants import find_best_matches_for_grants
from model import generate_grant_application

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


@app.get("/get-message")
async def test():
    '''
    No args get api call to test if fastapi is working
    '''
    return { "message": "Congrats! The app is running!" }


@app.post("/grants")
async def get_list(request: UserRequest):
    '''
    Input:
    request: contains the category, eligibility
    Output:
    returns: list of grants for the requested input
    '''
    if request.category == None or len(request.category) == 0:
        return { "status": "failure", "response": "Category required" }
    if request.eligibility == None or len(request.eligibility) == 0:
        return { "status": "failure", "response": "Eligibility required" }
    return find_best_matches_for_grants(request.category, request.eligibility)


@app.post("/generate/grant/{grant_id}/form")
async def get_list(grant_id:int, request: GenerateGrantRequest):
    return generate_grant_application(grant_id, request)
