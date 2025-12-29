from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
import app.services.regimen as regimen_service
from app.schemas.regimen import RegimenCreate, RegimenResponse
from typing import List

router = APIRouter(prefix="/regimenes", tags=["Regimenes"])

@router.get("/", response_model=List[RegimenResponse])
def listar_regimenes(db: Session = Depends(get_db)):
    return regimen_service.get_regimenes(db)

@router.get("/{regimen_id}", response_model=RegimenResponse)
def obtener_regimen(regimen_id: int, db: Session = Depends(get_db)):
    regimen = regimen_service.get_regimen(db, regimen_id)
    if not regimen:
        raise HTTPException(status_code=404, detail="Régimen no encontrado")
    return regimen

@router.post("/", response_model=RegimenResponse)
def crear_regimen(regimen: RegimenCreate, db: Session = Depends(get_db)):
    return regimen_service.create_regimen(db, regimen)

@router.delete("/{regimen_id}")
def eliminar_regimen(regimen_id: int, db: Session = Depends(get_db)):
    regimen = regimen_service.delete_regimen(db, regimen_id)
    if not regimen:
        raise HTTPException(status_code=404, detail="Régimen no encontrado")
    return {"message": "Régimen eliminado con éxito"}