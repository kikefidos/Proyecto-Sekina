from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.clase import ClaseOut, ClaseCreate, ClaseUpdate
from app.services import clase as service

router = APIRouter(prefix="/clases", tags=["Clases"])

@router.get("/", response_model=List[ClaseOut])
def listar_clases(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return service.get_clases(db, skip, limit)

@router.get("/{clase_id}", response_model=ClaseOut)
def obtener_clase(clase_id: int, db: Session = Depends(get_db)):
    db_clase = service.get_clase(db, clase_id)
    if not db_clase:
        raise HTTPException(status_code=404, detail="Clase no encontrada")
    return db_clase

@router.post("/", response_model=ClaseOut)
def crear_clase(clase: ClaseCreate, db: Session = Depends(get_db)):
    return service.create_clase(db, clase)

@router.put("/{clase_id}", response_model=ClaseOut)
def actualizar_clase(clase_id: int, clase: ClaseUpdate, db: Session = Depends(get_db)):
    db_clase = service.update_clase(db, clase_id, clase)
    if not db_clase:
        raise HTTPException(status_code=404, detail="Clase no encontrada")
    return db_clase

@router.delete("/{clase_id}", response_model=ClaseOut)
def eliminar_clase(clase_id: int, db: Session = Depends(get_db)):
    db_clase = service.delete_clase(db, clase_id)
    if not db_clase:
        raise HTTPException(status_code=404, detail="Clase no encontrada")
    return db_clase