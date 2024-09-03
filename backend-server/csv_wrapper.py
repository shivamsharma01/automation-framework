import os
import pandas as pd
from io import StringIO
from fastapi.responses import StreamingResponse
from mistral import assert_rows

FILE_PATH = "./files"
def get_csv_response(filename):
    '''
    Input:
    filename: name of the csv file
    Output:
    csv: the desired csv file
    '''
    df = pd.read_csv(f"{FILE_PATH}/{filename}.csv")
    response = StreamingResponse(StringIO(df.to_csv(index=False)), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=export.csv"
    return response

def get_json_response(filename):
    '''
    Input:
    filename: name of the csv file
    Output:
    csv: the csv file response in json format
    '''
    df = pd.read_csv(f"{FILE_PATH}/{filename}.csv")
    return { "headers": list(df.columns), "items": df.values.tolist() }

def create_csv(filename, file_content):
    '''
    Input:
    filename: name of the csv file
    file_content: content to write to the csv file
    '''
    with open(f"{FILE_PATH}/{filename}.csv", mode="wb") as csv_file:
        content_str = file_content.decode('utf-8')
        buffer = StringIO(content_str)
        csv_file.write(buffer.getvalue().encode('utf-8'))
        buffer.close()

def validate_csv(filename):
    '''
    Input:
    filename: name of the csv file
    Exception: remove the csv file and raise an exception if the csv is not in the desired format
    '''
    if pd.read_csv(f"{FILE_PATH}/{filename}.csv").columns.size != 3:
        os.remove(filename)
        raise Exception("Requires three columns - Question, Expected Answer, Keyword") 
    
def assert_csv(filename):
    '''
    Input:
    filename: name of the csv file
    Output:
    asserted_row: returns the assertion 1 and 2 response on the input 
    '''
    df = pd.read_csv(f"{FILE_PATH}/{filename}.csv")
    input_data = df.iloc[:, :3].values.tolist()
    return assert_rows(input_data, filename)

def write_asserted_csv(headers, data, filename):
    '''
    Input:
    headers: the headers to add in the csv
    data: the data to add in the csv
    filename: name of the csv file
    '''
    pd.DataFrame(data, columns=headers).to_csv(f"{FILE_PATH}/{filename}.csv", index=False)