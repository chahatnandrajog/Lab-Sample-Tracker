from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import Base, engine, SessionLocal
from app import schemas, crud, models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Lab Sample Tracking System")


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {
        "message": "Lab Sample Tracking System"
    }


@app.post("/samples/", response_model=schemas.SampleResponse)
def create_sample(sample: schemas.SampleCreate, db: Session = Depends(get_db)):
    existing_sample = crud.get_sample_by_sample_id(db, sample.sample_id)

    if existing_sample:
        raise HTTPException(status_code=400, detail="Sample ID already exists")

    return crud.create_sample(db, sample)


@app.get("/samples/", response_model=list[schemas.SampleResponse])
def list_samples(db: Session = Depends(get_db)):
    return crud.get_samples(db)


@app.get("/samples/{sample_id}", response_model=schemas.SampleResponse)
def get_sample(sample_id: str, db: Session = Depends(get_db)):
    sample = crud.get_sample_by_sample_id(db, sample_id)

    if sample is None:
        raise HTTPException(status_code=404, detail="Sample not found")

    return sample


@app.patch("/samples/{sample_id}/status", response_model=schemas.SampleResponse)
def update_status(sample_id: str, new_status: str, db: Session = Depends(get_db)):
    sample = crud.update_sample_status(db, sample_id, new_status)

    if sample is None:
        raise HTTPException(status_code=404, detail="Sample not found")

    return sample