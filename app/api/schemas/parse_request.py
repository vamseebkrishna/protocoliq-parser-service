from pydantic import BaseModel
from typing import Optional

class EligibilityParseRequest(BaseModel):
    protocolId: Optional[str] = None
    rawText: str
