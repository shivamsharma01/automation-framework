from pydantic import BaseModel
from typing import List

'''
Request structure to take user input
'''
class UserRequest(BaseModel):
    category: List[str]
    eligibility: List[str]
    location: str
