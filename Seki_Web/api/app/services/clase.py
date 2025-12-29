from sqlalchemy.orm import Session
from app.models.clase import Clase
from app.schemas.clase import ClaseCreate, ClaseUpdate

def get_clases(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Clase).offset(skip).limit(limit).all()

def get_clase(db: Session, clase_id: int):
    return db.query(Clase).filter(Clase.id == clase_id).first()

def create_clase(db: Session, clase: ClaseCreate):
    db_clase = Clase(**clase.dict())
    db.add(db_clase)
    db.commit()
    db.refresh(db_clase)
    return db_clase

def update_clase(db: Session, clase_id: int, clase: ClaseUpdate):
    db_clase = get_clase(db, clase_id)
    if not db_clase:
        return None
    for key, value in clase.dict(exclude_unset=True).items():
        setattr(db_clase, key, value)
    db.commit()
    db.refresh(db_clase)
    return db_clase

def delete_clase(db: Session, clase_id: int):
    db_clase = get_clase(db, clase_id)
    if not db_clase:
        return None
    db.delete(db_clase)
    db.commit()
    return db_clase