from sqlalchemy.orm import Session
from app.models.universidad import Universidad
from app.schemas.universidad import UniversidadCreate, UniversidadUpdate

def get_universidades(db: Session):
    return db.query(Universidad).all()

def get_universidad(db: Session, universidad_id: int):
    return db.query(Universidad).filter(Universidad.id == universidad_id).first()

def create_universidad(db: Session, universidad: UniversidadCreate):
    db_uni = Universidad(**universidad.dict())
    db.add(db_uni)
    db.commit()
    db.refresh(db_uni)
    return db_uni

def update_universidad(db: Session, universidad_id: int, universidad: UniversidadUpdate):
    db_uni = get_universidad(db, universidad_id)
    if db_uni:
        for key, value in universidad.dict().items():
            setattr(db_uni, key, value)
        db.commit()
        db.refresh(db_uni)
    return db_uni

def delete_universidad(db: Session, universidad_id: int):
    db_uni = get_universidad(db, universidad_id)
    if db_uni:
        db.delete(db_uni)
        db.commit()
    return db_uni