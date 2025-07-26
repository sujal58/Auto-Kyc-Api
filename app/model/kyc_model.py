from pydantic import BaseModel
from typing import Optional
from datetime import date

class KycRequest(BaseModel):
    document_front_path: str
    document_back_path: str
    user_image_path: str
    name: str
    document_number: str
    address: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    document_type: Optional[str] = None
    dob: Optional[date] = None