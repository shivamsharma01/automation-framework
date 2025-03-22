from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from request_model import UserRequest
from grants import find_best_matches_for_grants

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
