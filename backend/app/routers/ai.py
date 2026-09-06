from fastapi import APIRouter
from app.schemas.ai import PromptRequest, SummaryResponse

router = APIRouter(prefix="/ai", tags=["AI"])

@router.post("/summarize", response_model=SummaryResponse)
async def summarize_text(user_input: PromptRequest):

    return {
        "summary": f"Summary of the text: {user_input.text[:50]}...",
        "key_points":[
            "Main point",
            "Secondary point", 
            "Additional point"]
    }