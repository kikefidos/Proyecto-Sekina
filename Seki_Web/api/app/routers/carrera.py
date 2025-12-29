from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.carrera import CarreraCreate, CarreraUpdate, CarreraResponse
from app.services import carrera as carrera_service
from app.core.database import get_db

router = APIRouter(prefix="/api/carreras", tags=["Carreras"])

@router.get("/", response_model=list[CarreraResponse])
def get_all(db: Session = Depends(get_db)):
    return carrera_service.get_carreras(db)

@router.get("/{carrera_id}", response_model=CarreraResponse)
def get_one(carrera_id: int, db: Session = Depends(get_db)):
    car = carrera_service.get_carrera(db, carrera_id)
    if not car:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")
    return car

@router.post("/", response_model=CarreraResponse)
def create(carrera_in: CarreraCreate, db: Session = Depends(get_db)):
    return carrera_service.create_carrera(db, carrera_in)

@router.put("/{carrera_id}", response_model=CarreraResponse)
def update(carrera_id: int, carrera_in: CarreraUpdate, db: Session = Depends(get_db)):
    car = carrera_service.update_carrera(db, carrera_id, carrera_in)
    if not car:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")
    return car

@router.delete("/{carrera_id}")
def delete(carrera_id: int, db: Session = Depends(get_db)):
    car = carrera_service.delete_carrera(db, carrera_id)
    if not car:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")
    return {"message": "Carrera eliminada correctamente"}