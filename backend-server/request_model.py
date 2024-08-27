from pydantic import BaseModel

class UserRequest(BaseModel):
    question: str
    expected: str
    keyword: str
