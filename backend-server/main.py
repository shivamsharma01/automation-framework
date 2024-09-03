from fastapi import FastAPI, File, UploadFile, BackgroundTasks
import uuid
from fastapi.middleware.cors import CORSMiddleware
from db import get_db
from tinydb import Query
from csv_wrapper import get_csv_response, get_json_response, create_csv, validate_csv, assert_csv, write_asserted_csv
from request_model import UserRequest
from mistral import assert_row

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

def get_headers():
    '''
    Output:
    Headers: Headers to display in the output csv
    '''
    return ['Question', 'Expected Response', 'Actual Response', 'Keyword', 'Assertion 1 (Fuzzy)', 'Assertion 1 (Text Emb..)', 'Assertion 2 LLM', 'Assertion 2 contains']
        
def process_file(filename: str):
    '''
    Background task that write input csv to file storeage and 
    initiates the flow to assert input csv and 
    replace it with the asserted csv to download and query later
    '''
    DB = get_db()
    DB.update({'status': 'processing'}, Query().id == filename)
    
    try:
        asserted_csv_data = assert_csv(filename)
        write_asserted_csv(get_headers(), asserted_csv_data, filename)
        DB.update({'status': 'complete', 'percent': 100 }, Query().id == filename)
    except Exception as e:
        print(f"Failed to process file {filename}: {e}")
        DB.update({'status': 'failed'}, Query().id == filename)

@app.get("/get-message")
async def test():
    '''
    No args get api call to test if fastapi is working
    '''
    return { "message": "Congrats! The app is running!" }


@app.put("/uploadcsv")
async def upload(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    '''
    Upload the file and return a uuid that the client then uses to view/download results later
    '''
    myuuid = str(uuid.uuid4())
    file_content = await file.read()
    DB = get_db()
    DB.insert({ 'id': myuuid, 'percent': 0, 'status': 'pending'})
    try:
        create_csv(myuuid, file_content)
        validate_csv(myuuid)
        background_tasks.add_task(process_file, myuuid)
    except Exception as e:
        print(f"Failed to process file {myuuid}: {e}")
        DB.update({'status': 'failed'}, Query().id == myuuid)
    return { "uuid": myuuid }


@app.get("/status/{file_id}")
async def get_status(file_id: str):
    '''
    Check the status of the file processing.
    '''
    DB = get_db()
    rows = DB.search(Query().id == file_id)
    
    if len(rows) > 0:
        return {"status": rows[0]['status'], "percent": rows[0]['percent']}
    else:
        return {"status": "not found"}
    

@app.get("/download/{file_id}")
async def file_download(file_id: str):
    '''
    Download the csv file.
    '''
    DB = get_db()
    rows = DB.search(Query().id == file_id)
    if len(rows) > 0:
        status = rows[0]['status']
        if status == "complete":
            return get_csv_response(file_id)
        else:
            return { "status" : status }
    else:
        return {"status": "not found"}


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
            return get_json_response(file_id)
        else:
            return { "status" : status }
    else:
        return {"status": "not found"}


@app.post("/user/input")
async def create_item(request: UserRequest):
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

    return { "headers": get_headers(), "items": [assert_row(request.question, request.expected, request.keyword)] }
