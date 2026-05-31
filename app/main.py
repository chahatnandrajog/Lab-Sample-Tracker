from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import UploadFile, File
import pandas as pd

from app.database import Base, engine, SessionLocal
from app import schemas, crud, models

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.ai_service import generate_sample_summary

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Lab Sample Tracking System")
app.mount("/static", StaticFiles(directory="static"), name="static")


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return FileResponse("static/index.html")


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


@app.post("/upload-csv/")
def upload_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    df = pd.read_csv(file.file)

    required_columns = [
        "sample_id",
        "sample_type",
        "collection_date",
        "status",
        "storage_location",
        "owner",
        "temperature",
        "notes"
    ]

    errors = []
    imported = 0
    duplicates_skipped = 0

    for column in required_columns:
        if column not in df.columns:
            raise HTTPException(
                status_code=400,
                detail=f"Missing required column: {column}"
            )

    for index, row in df.iterrows():
        row_number = index + 2

        row_has_error = False

        for column in required_columns:
            if pd.isna(row[column]) or str(row[column]).strip() == "":
                errors.append(
                    f"Row {row_number}: missing value for {column}"
                )
                row_has_error = True

        if row_has_error:
            continue

        try:
            temperature = float(row["temperature"])
        except (ValueError, TypeError):
            errors.append(
                f"Row {row_number}: temperature must be a number"
            )
            continue

        if temperature < -200 or temperature > 100:
            errors.append(
                f"Row {row_number}: temperature {temperature} is outside valid range"
            )
            continue

        existing_sample = crud.get_sample_by_sample_id(
            db,
            row["sample_id"]
        )

        if existing_sample:
            duplicates_skipped += 1
            errors.append(
                f"Row {row_number}: duplicate sample_id {row['sample_id']}"
            )
            continue

        sample = schemas.SampleCreate(
            sample_id=row["sample_id"],
            sample_type=row["sample_type"],
            collection_date=row["collection_date"],
            status=row["status"],
            storage_location=row["storage_location"],
            owner=row["owner"],
            temperature=temperature,
            notes=row["notes"]
        )

        crud.create_sample(db, sample)
        imported += 1

    return {
        "imported_samples": imported,
        "duplicates_skipped": duplicates_skipped,
        "errors": errors
    }

@app.get("/dashboard/summary")
def dashboard_summary(db: Session = Depends(get_db)):
    return crud.get_dashboard_summary(db)

@app.get("/samples/{sample_id}/ai-summary")
def ai_summary(
    sample_id: str,
    db: Session = Depends(get_db)
):

    sample = crud.get_sample_by_sample_id(
        db,
        sample_id
    )

    if sample is None:
        raise HTTPException(
            status_code=404,
            detail="Sample not found"
        )

    summary = generate_sample_summary(sample)

    return {
        "sample_id": sample_id,
        "ai_summary": summary
    }