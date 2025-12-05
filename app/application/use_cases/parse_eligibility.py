from datetime import datetime
from app.api.schemas.parse_request import EligibilityParseRequest
from app.api.schemas.parse_response import EligibilityParseResponse, Criterion, Metadata

class ParseEligibilityUseCase:

    def __init__(self, ai_service):
        self.ai_service = ai_service

    def execute(self, request: EligibilityParseRequest) -> EligibilityParseResponse:
        """
        Main entry point for the use case.
        Calls the AI service, parses output, and returns structured response.
        """

        # TEMP MOCK UNTIL AI KEY SET — prevents crashes
        mock_criteria = [
            Criterion(
                criterionId="1",
                raw=request.rawText,
                type="INCLUSION",
                normalized="Mock normalized text",
                structuredRule={"field": "age", "operator": ">=", "value": 18}
            )
        ]

        return EligibilityParseResponse(
            criteria=mock_criteria,
            metadata=Metadata(
                modelVersion="mock-v1",
                parseTimestamp=datetime.utcnow()
            )
        )
