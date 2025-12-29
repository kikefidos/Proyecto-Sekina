from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.carrera_universidad import CarreraUniversidadCreate, CarreraUniversidadResponse
from app.services import carrera_universidad as service
from app.core.database import get_db

router = APIRouter(prefix="/api/carrera_universidad", tags=["Carrera-Universidad"])

# Crear relación
@router.post("/", response_model=CarreraUniversidadResponse)
def create_relacion(relacion: CarreraUniversidadCreate, db: Session = Depends(get_db)):
    result = service.create_relacion(db, relacion.carrera_id, relacion.universidad_id)
    if not result:
        raise HTTPException(status_code=404, detail="Carrera o Universidad no encontrada")
    return result

# Listar universidades por carrera
@router.get("/by_carrera/{carrera_id}")
def get_universidades(carrera_id: int, db: Session = Depends(get_db)):
    result = service.get_universidades_by_carrera(db, carrera_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")
    return result

# Listar carreras por universidad
@router.get("/by_universidad/{universidad_id}")
def get_carreras(universidad_id: int, db: Session = Depends(get_db)):
    result = service.get_carreras_by_universidad(db, universidad_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Universidad no encontrada")
    return result

# Eliminar relación
@router.delete("/")
def delete_relacion(relacion: CarreraUniversidadCreate, db: Session = Depends(get_db)):
    ok = service.delete_relacion(db, relacion.carrera_id, relacion.universidad_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Relación no encontrada")
    return {"message": "Relación eliminada correctamente"}