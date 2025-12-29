from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.rol import RolCreate, RolOut, RolUpdate
from app.services import rol_service

router = APIRouter(prefix="/roles", tags=["Roles"])

@router.get("/", response_model=list[RolOut])
def listar_roles(db: Session = Depends(get_db)):
    return rol_service.get_roles(db)

@router.get("/{rol_id}", response_model=RolOut)
def obtener_rol(rol_id: int, db: Session = Depends(get_db)):
    rol = rol_service.get_rol(db, rol_id)
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return rol

@router.post("/", response_model=RolOut)
def crear_rol(rol: RolCreate, db: Session = Depends(get_db)):
    return rol_service.create_rol(db, rol)

@router.put("/{rol_id}", response_model=RolOut)
def actualizar_rol(rol_id: int, rol: RolUpdate, db: Session = Depends(get_db)):
    actualizado = rol_service.update_rol(db, rol_id, rol)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return actualizado

@router.delete("/{rol_id}", response_model=RolOut)
def eliminar_rol(rol_id: int, db: Session = Depends(get_db)):
    eliminado = rol_service.delete_rol(db, rol_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return eliminado