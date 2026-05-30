from sqlalchemy.orm import Session
from app import models, schemas

def create_sample(db: Session, sample: schemas.SampleCreate):
    db_sample = models.Sample(**sample.model_dump())

    db.add(db_sample)
    db.commit()
    db.refresh(db_sample)

    return db_sample

def get_samples(db: Session):
    return db.query(models.Sample).all()

def get_sample_by_sample_id(db: Session, sample_id: str)
    return db.query(models.Sample).filter(
        models.Sample.sample_id == sample_id
    ).first()

def update_sample_status(db: Session, sample_id: str, new_status: str):
    sample = get_sample_by_sample_id(db, sample_id)

    if sample is None:
        return None
    
    sample.status = new_status
    db.commit()
    db.refresh(sample)

    return sample