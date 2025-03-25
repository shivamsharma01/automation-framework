from pydantic import BaseModel
from typing import List


class UserRequest(BaseModel):
    category: List[str]
    eligibility: List[str]


class GenerateGrantRequest(BaseModel):
    fullName: str
    email: str
    organizationName: str
    projectName: str
    purpose: str
    fundingAmount: str
    expectedOutcomes: str
    targetAudience: str