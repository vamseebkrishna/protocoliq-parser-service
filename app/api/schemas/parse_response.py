from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Metadata(BaseModel):
    modelVersion: Optional[str] = None
    parseTimestamp: Optional[datetime] = None

class Criterion(BaseModel):
    criterionId: Optional[str] = None
    raw: str
    type: str          # "INCLUSION" or "EXCLUSION"
    normalized: Optional[str] = None
    structuredRule: Optional[dict] = None

class EligibilityParseResponse(BaseModel):
    criteria: List[Criterion]
    metadata: Optional[Metadata] = None
