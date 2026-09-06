from pydantic import BaseModel

class PromptRequest(BaseModel):
    text: str

class SummaryResponse(BaseModel):
    summary: str
    