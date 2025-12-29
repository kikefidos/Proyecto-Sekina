from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.facultad import FacultadOut, FacultadCreate, FacultadUpdate
from app.services import facultad as service

router = APIRouter(prefix="/facultades", tags=["Facultades"])

@router.get("/", response_model=List[FacultadOut])
def listar_facultades(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return service.get_facultades(db, skip, limit)

@router.get("/{facultad_id}", response_model=FacultadOut)
def obtener_facultad(facultad_id: int, db: Session = Depends(get_db)):
    db_facultad = service.get_facultad(db, facultad_id)
    if not db_facultad:
        raise HTTPException(status_code=404, detail="Facultad no encontrada")
    return db_facultad

@router.post("/", response_model=FacultadOut)
def crear_facultad(facultad: FacultadCreate, db: Session = Depends(get_db)):
    return service.create_facultad(db, facultad)

@router.put("/{facultad_id}", response_model=FacultadOut)
def actualizar_facultad(facultad_id: int, facultad: FacultadUpdate, db: Session = Depends(get_db)):
    db_facultad = service.update_facultad(db, facultad_id, facultad)
    if not db_facultad:
        raise HTTPException(status_code=404, detail="Facultad no encontrada")
    return db_facultad

@router.delete("/{facultad_id}", response_model=FacultadOut)
def eliminar_facultad(facultad_id: int, db: Session = Depends(get_db)):
    db_facultad = service.delete_facultad(db, facultad_id)
    if not db_facultad:
        raise HTTPException(status_code=404, detail="Facultad no encontrada")
    return db_facultad