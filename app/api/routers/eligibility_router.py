from fastapi import APIRouter
from app.api.schemas.parse_request import EligibilityParseRequest
from app.api.schemas.parse_response import EligibilityParseResponse
from app.application.use_cases.parse_eligibility import ParseEligibilityUseCase

router = APIRouter(tags=["Eligibility"])

@router.post("/parse/eligibility", response_model=EligibilityParseResponse)
def parse_eligibility(request: EligibilityParseRequest):
    # Import locally to prevent blocking app startup
    from app.infrastructure.ai.openai_adapter import OpenAIAdapter

    ai_service = OpenAIAdapter()
    use_case = ParseEligibilityUseCase(ai_service)
    return use_case.execute(request)
