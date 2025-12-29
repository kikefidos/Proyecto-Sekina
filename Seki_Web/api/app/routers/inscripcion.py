from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.inscripcion import InscripcionOut, InscripcionCreate, InscripcionUpdate
from app.services import inscripcion as service

router = APIRouter(prefix="/inscripciones", tags=["Inscripciones"])

@router.get("/", response_model=List[InscripcionOut])
def listar_inscripciones(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return service.get_inscripciones(db, skip, limit)

@router.get("/{inscripcion_id}", response_model=InscripcionOut)
def obtener_inscripcion(inscripcion_id: int, db: Session = Depends(get_db)):
    db_inscripcion = service.get_inscripcion(db, inscripcion_id)
    if not db_inscripcion:
        raise HTTPException(status_code=404, detail="Inscripción no encontrada")
    return db_inscripcion

@router.post("/", response_model=InscripcionOut)
def crear_inscripcion(inscripcion: InscripcionCreate, db: Session = Depends(get_db)):
    return service.create_inscripcion(db, inscripcion)

@router.put("/{inscripcion_id}", response_model=InscripcionOut)
def actualizar_inscripcion(inscripcion_id: int, inscripcion: InscripcionUpdate, db: Session = Depends(get_db)):
    db_inscripcion = service.update_inscripcion(db, inscripcion_id, inscripcion)
    if not db_inscripcion:
        raise HTTPException(status_code=404, detail="Inscripción no encontrada")
    return db_inscripcion

@router.delete("/{inscripcion_id}", response_model=InscripcionOut)
def eliminar_inscripcion(inscripcion_id: int, db: Session = Depends(get_db)):
    db_inscripcion = service.delete_inscripcion(db, inscripcion_id)
    if not db_inscripcion:
        raise HTTPException(status_code=404, detail="Inscripción no encontrada")
    return db_inscripcion