from fastapi import FastAPI, File, UploadFile, BackgroundTasks
import uuid
from fastapi.middleware.cors import CORSMiddleware
from db import get_db
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
    Used by csv and user input as header of the response
    '''
    return ['Question', 'Expected Response', 'Actual Response', 'Keyword', 'Assertion 1 (Fuzzy)', 'Assertion 1 (Text Emb..)', 'Assertion 2 LLM', 'Assertion 2 contains']
        
def process_file(filename: str):
    '''
    Background task that write input csv to file storeage and 
    initiates the flow to assert input csv and 
    replace it with the asserted csv to download and query later
    '''
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE file_status SET status = ? WHERE id = ?", ("processing", filename))
    conn.commit()
        
    try:
        asserted_csv_data = assert_csv(filename)
        write_asserted_csv(get_headers(), asserted_csv_data, filename)
        cursor.execute("UPDATE file_status SET status = ?, percent = 100 WHERE id = ?", ("complete", filename))
        conn.commit()
    except Exception as e:
        print(f"Failed to process file {filename}: {e}")
        cursor.execute("UPDATE file_status SET status = ? WHERE id = ?", ("failed", filename))
        conn.commit()

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
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO file_status (id, percent, status) VALUES (?, ?, ?)", (myuuid, 0, "pending"))
    conn.commit()
    try:
        create_csv(myuuid, file_content)
        validate_csv(myuuid)
        background_tasks.add_task(process_file, myuuid)
    except Exception as e:
        print(f"Failed to process file {myuuid}: {e}")
        cursor.execute("UPDATE file_status SET status = ? WHERE id = ?", ("failed", myuuid))
        conn.commit()
    return { "uuid": myuuid }


@app.get("/status/{file_id}")
async def get_status(file_id: str):
    '''
    Check the status of the file processing.
    '''
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT status, percent FROM file_status WHERE id = ?", (file_id,))
    row = cursor.fetchone()
    if row:
        return {"status": row[0], "percent": row[1]}
    else:
        return {"status": "not found"}
    

@app.get("/download/{file_id}")
async def file_download(file_id: str):
    '''
    Download the csv file.
    '''
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT status, percent FROM file_status WHERE id = ?", (file_id,))
    row = cursor.fetchone()
    if row:
        status = row[0] 
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
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT status, percent FROM file_status WHERE id = ?", (file_id,))
    row = cursor.fetchone()    
    if row:
        status = row[0] 
        if status == "complete":
            return get_json_response(file_id)
        else:
            return { "status" : status }
    else:
        return {"status": "not found"}


@app.post("/user/input")
async def create_item(request: UserRequest):
    if request.question == None or request.question == '':
        return { "status": "failure", "response": "Question required" }
    if request.expected == None or request.expected == '':
        return { "status": "failure", "response": "Expected Response required" }
    if request.keyword == None or request.keyword == '':
        return { "status": "failure", "response": "Keyword required for Assertion 2" }

    return { "headers": get_headers(), "items": [assert_row(request.question, request.expected, request.keyword)] }
