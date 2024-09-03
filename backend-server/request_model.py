from pydantic import BaseModel

'''
Request structure to take user input
'''
class UserRequest(BaseModel):
    question: str
    expected: str
    keyword: str
