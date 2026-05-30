from pydantic import BaseModel
from typing import Optional

class SampleCreate(BaseModel):
    sample_id: str
    sample_type: str
    collection_date: str
    status: str
    storage_location: str
    owner: str
    temperature: float
    notes: Optional[str] = None

class SampleResponse(SampleCreate):
    id: int

    class Config:
        from_attributes = True