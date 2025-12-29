from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.universidad import UniversidadCreate, UniversidadUpdate, UniversidadResponse
from app.services import universidad as universidad_service   # 👈 alias
from app.core.database import get_db

router = APIRouter(prefix="/api/universidades", tags=["Universidades"])

@router.get("/", response_model=list[UniversidadResponse])
def get_all(db: Session = Depends(get_db)):
    return universidad_service.get_universidades(db)

@router.get("/{universidad_id}", response_model=UniversidadResponse)
def get_one(universidad_id: int, db: Session = Depends(get_db)):
    uni = universidad_service.get_universidad(db, universidad_id)
    if not uni:
        raise HTTPException(status_code=404, detail="Universidad no encontrada")
    return uni

@router.post("/", response_model=UniversidadResponse)
def create(universidad: UniversidadCreate, db: Session = Depends(get_db)):
    return universidad_service.create_universidad(db, universidad)

@router.put("/{universidad_id}", response_model=UniversidadResponse)
def update(universidad_id: int, universidad: UniversidadUpdate, db: Session = Depends(get_db)):
    uni = universidad_service.update_universidad(db, universidad_id, universidad)
    if not uni:
        raise HTTPException(status_code=404, detail="Universidad no encontrada")
    return uni

@router.delete("/{universidad_id}")
def delete(universidad_id: int, db: Session = Depends(get_db)):
    uni = universidad_service.delete_universidad(db, universidad_id)
    if not uni:
        raise HTTPException(status_code=404, detail="Universidad no encontrada")
    return {"message": "Universidad eliminada correctamente"}