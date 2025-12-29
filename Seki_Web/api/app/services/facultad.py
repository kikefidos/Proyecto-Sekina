from sqlalchemy.orm import Session
from app.models.facultad import Facultad
from app.schemas.facultad import FacultadCreate, FacultadUpdate

def get_facultades(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Facultad).offset(skip).limit(limit).all()

def get_facultad(db: Session, facultad_id: int):
    return db.query(Facultad).filter(Facultad.id == facultad_id).first()

def create_facultad(db: Session, facultad: FacultadCreate):
    db_facultad = Facultad(**facultad.dict())
    db.add(db_facultad)
    db.commit()
    db.refresh(db_facultad)
    return db_facultad

def update_facultad(db: Session, facultad_id: int, facultad: FacultadUpdate):
    db_facultad = get_facultad(db, facultad_id)
    if not db_facultad:
        return None
    for key, value in facultad.dict(exclude_unset=True).items():
        setattr(db_facultad, key, value)
    db.commit()
    db.refresh(db_facultad)
    return db_facultad

def delete_facultad(db: Session, facultad_id: int):
    db_facultad = get_facultad(db, facultad_id)
    if not db_facultad:
        return None
    db.delete(db_facultad)
    db.commit()
    return db_facultad