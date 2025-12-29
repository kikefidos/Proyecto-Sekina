from sqlalchemy.orm import Session
from app.models.regimen import Regimen
from app.schemas.regimen import RegimenCreate

def get_regimenes(db: Session):
    return db.query(Regimen).all()

def get_regimen(db: Session, regimen_id: int):
    return db.query(Regimen).filter(Regimen.id == regimen_id).first()

def create_regimen(db: Session, regimen: RegimenCreate):
    db_regimen = Regimen(**regimen.dict())
    db.add(db_regimen)
    db.commit()
    db.refresh(db_regimen)
    return db_regimen

def delete_regimen(db: Session, regimen_id: int):
    regimen = db.query(Regimen).filter(Regimen.id == regimen_id).first()
    if regimen:
        db.delete(regimen)
        db.commit()
    return regimen