from sqlalchemy.orm import Session
from app.models.inscripciones_plataforma import InscripcionPlataforma
from app.schemas.inscripciones_plataforma import (
    InscripcionPlataformaCreate,
    InscripcionPlataformaUpdate,
)

def listar_inscripciones(db: Session):
    return db.query(InscripcionPlataforma).all()

def obtener_inscripcion(db: Session, inscripcion_id: int):
    return db.query(InscripcionPlataforma).filter(InscripcionPlataforma.id == inscripcion_id).first()

def crear_inscripcion(db: Session, inscripcion: InscripcionPlataformaCreate):
    db_inscripcion = InscripcionPlataforma(**inscripcion.dict())
    db.add(db_inscripcion)
    db.commit()
    db.refresh(db_inscripcion)
    return db_inscripcion

def actualizar_inscripcion(db: Session, inscripcion_id: int, inscripcion: InscripcionPlataformaUpdate):
    db_inscripcion = obtener_inscripcion(db, inscripcion_id)
    if not db_inscripcion:
        return None
    for key, value in inscripcion.dict(exclude_unset=True).items():
        setattr(db_inscripcion, key, value)
    db.commit()
    db.refresh(db_inscripcion)
    return db_inscripcion

def eliminar_inscripcion(db: Session, inscripcion_id: int):
    db_inscripcion = obtener_inscripcion(db, inscripcion_id)
    if db_inscripcion:
        db.delete(db_inscripcion)
        db.commit()
        return True
    return False