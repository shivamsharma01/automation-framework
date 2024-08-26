import uvicorn
from fastapi import FastAPI, File, UploadFile, BackgroundTasks
from io import StringIO
import uuid
import sqlite3
import threading
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from mistral import get_response, DriverManager


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

class UserRequest(BaseModel):
    question: str
    expected: str
    keyword: str

thread_local = threading.local()

def get_db():
    if not hasattr(thread_local, "conn"):
        thread_local.conn = sqlite3.connect(':memory:')
        cursor = thread_local.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS file_status (
                id TEXT PRIMARY KEY,
                percent INTEGER,
                status TEXT
            )
        ''')
        thread_local.conn.commit()
    return thread_local.conn


@app.get("/get-message")
async def read_root():
    return { "message": "Congrats! This is your first API!" }


@app.put("/uploadcsv")
async def upload(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    '''
    Upload the file and return a uuid that the client then uses to view/download results later
    '''
    myuuid = uuid.uuid4()
    file_content = await file.read()
    background_tasks.add_task(process_file, str(myuuid), file_content)

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO file_status (id, percent, status) VALUES (?, ?, ?)", (str(myuuid), 0, "pending"))
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
    if row[1] != 100:
        if row[1] == 90:    
            cursor.execute("UPDATE file_status SET status = ?, percent = percent + ? WHERE id = ?", ("complete", 10, file_id))
        else:
            cursor.execute("UPDATE file_status SET percent = percent + ? WHERE id = ?", (10, file_id))
        conn.commit()
    if row:
        return {"status": row[0], "percent": row[1]}
    else:
        return {"status": "not_found"}
    

@app.get("/download/{file_id}")
async def file_download(file_id: str):
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
            df = pd.read_csv(f"files/{file_id}.csv")
            response = StreamingResponse(StringIO(df.to_csv(index=False)), media_type="text/csv")
            response.headers["Content-Disposition"] = "attachment; filename=export.csv"
            return response
        else:
            return { "status" : status }
    else:
        return {"status": "not_found"}


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
            df = pd.read_csv(f"files/{file_id}.csv")
            headers = list(df.columns)
            items = df.values.tolist()
            return { "headers": headers, "items": items }
        else:
            return { "status" : status }
    else:
        return {"status": "not_found"}


@app.post("/user/model")
async def create_item(request: UserRequest):
    driver_manager = DriverManager()
    driver_manager.init()
    
    headers = ['Question', 'Expected Response', 'Actual Response', 'Keyword']
    items = [[request.question, request.expected, get_response(request.question, driver_manager), request.keyword]]
    
    driver_manager.close()
    return { "headers": headers, "items": items }


def process_file(filename: str, file_content: bytes):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE file_status SET status = ? WHERE id = ?", ("processing", filename))
        conn.commit()
        with open(f"/app/files/{filename}.csv", mode="wb") as csv_file:
            content_str = file_content.decode('utf-8')
            buffer = StringIO(content_str)        
            csv_file.write(buffer.getvalue().encode('utf-8'))
        
        buffer.close()
        cursor.execute("UPDATE file_status SET status = ?, percent = 100 WHERE id = ?", ("complete", filename))
        conn.commit()
    except Exception as e:
        cursor.execute("UPDATE file_status SET status = ? WHERE id = ?", ("failed", filename))
        conn.commit()
        print(f"Failed to process file {filename}: {e}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)