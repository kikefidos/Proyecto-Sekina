from sqlalchemy.orm import Session
from app.models.carrera import Carrera
from app.models.universidad import Universidad
from app.schemas.carrera import CarreraCreate, CarreraUpdate

def get_carreras(db: Session):
    return db.query(Carrera).all()

def get_carrera(db: Session, carrera_id: int):
    return db.query(Carrera).filter(Carrera.id == carrera_id).first()

def create_carrera(db: Session, carrera: CarreraCreate):
    db_carrera = Carrera(nombre=carrera.nombre)
    db.add(db_carrera)
    db.commit()
    db.refresh(db_carrera)
    return db_carrera

def update_carrera(db: Session, carrera_id: int, carrera: CarreraUpdate):
    db_carrera = get_carrera(db, carrera_id)
    if not db_carrera:
        return None
    db_carrera.nombre = carrera.nombre
    db.commit()
    db.refresh(db_carrera)
    return db_carrera

def delete_carrera(db: Session, carrera_id: int):
    db_carrera = get_carrera(db, carrera_id)
    if not db_carrera:
        return None
    db.delete(db_carrera)
    db.commit()
    return db_carrera

