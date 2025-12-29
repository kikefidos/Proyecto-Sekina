from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.inscripciones_plataforma import (
    InscripcionPlataformaCreate,
    InscripcionPlataformaUpdate,
    InscripcionPlataformaOut,
)
import app.services.inscripciones_plataforma as inscripcion_service
from typing import List

router = APIRouter(prefix="/inscripciones_plataforma", tags=["Inscripciones Plataforma"])

@router.get("/", response_model=List[InscripcionPlataformaOut])
def listar_inscripciones(db: Session = Depends(get_db)):
    return inscripcion_service.listar_inscripciones(db)

@router.get("/{inscripcion_id}", response_model=InscripcionPlataformaOut)
def obtener_inscripcion(inscripcion_id: int, db: Session = Depends(get_db)):
    db_inscripcion = inscripcion_service.obtener_inscripcion(db, inscripcion_id)
    if not db_inscripcion:
        raise HTTPException(status_code=404, detail="Inscripción no encontrada")
    return db_inscripcion

@router.post("/", response_model=InscripcionPlataformaOut)
def crear_inscripcion(inscripcion: InscripcionPlataformaCreate, db: Session = Depends(get_db)):
    return inscripcion_service.crear_inscripcion(db, inscripcion)

@router.put("/{inscripcion_id}", response_model=InscripcionPlataformaOut)
def actualizar_inscripcion(inscripcion_id: int, inscripcion: InscripcionPlataformaUpdate, db: Session = Depends(get_db)):
    db_inscripcion = inscripcion_service.actualizar_inscripcion(db, inscripcion_id, inscripcion)
    if not db_inscripcion:
        raise HTTPException(status_code=404, detail="Inscripción no encontrada")
    return db_inscripcion

@router.delete("/{inscripcion_id}")
def eliminar_inscripcion(inscripcion_id: int, db: Session = Depends(get_db)):
    ok = inscripcion_service.eliminar_inscripcion(db, inscripcion_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Inscripción no encontrada")
    return {"ok": True, "mensaje": "Inscripción eliminada correctamente"}