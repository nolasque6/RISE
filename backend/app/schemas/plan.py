from datetime import date
from typing import Literal
from pydantic import BaseModel, Field

class PlanRequest(BaseModel):
    test: Literal ["SAT", "ACT", "TOEFL", "IELTS"]
