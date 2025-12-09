from app.application.pipelines.eligibility_pipeline import EligibilityPipeline
from app.api.schemas.parse_response import EligibilityParseResponse, Criterion, Metadata
from datetime import datetime

class ParseEligibilityUseCase:

    def __init__(self):
        self.pipeline = EligibilityPipeline()

    def execute(self, request):
        result = self.pipeline.run(request.rawText)

        criteria_models = [
            Criterion(
                criterionId=str(i + 1),
                raw=c["raw"],
                type=c["type"],
                normalized=c.get("normalized", c["raw"]),
                structuredRule=c.get("structuredRule", {})
            )
            for i, c in enumerate(result["criteria"])
        ]

        metadata = Metadata(
            modelVersion=result["metadata"]["modelVersion"],
            parseTimestamp=datetime.utcnow()
        )

        return EligibilityParseResponse(criteria=criteria_models, metadata=metadata)
