from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Sample(Base):
    __tablename__ = "samples"

    id = Column(Integer, primary_key=True, index=True)

    sample_id = Column(String, unique=True, index=True)

    sample_type = Column(String)

    collection_date = Column(String)

    status = Column(String)

    storage_location = Column(String)

    owner = Column(String)

    temperature = Column(Float)

    notes = Column(String)