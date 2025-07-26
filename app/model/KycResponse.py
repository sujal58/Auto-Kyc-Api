from pydantic import BaseModel, Field
from datetime import datetime


class KycVerificationResponse(BaseModel):
    status: str = Field(..., example="success")
    code: int = Field(..., example=200)
    message: str = Field(..., example="✅ KYC verified ✅")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    kyc_score: float = Field(..., example=0.32)
    confidence: float = Field(..., example=82.35)
