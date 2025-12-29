from sqlalchemy.orm import Session
from app.models.rol import Rol
from app.schemas.rol import RolCreate, RolUpdate

def get_roles(db: Session):
    return db.query(Rol).all()

def get_rol(db: Session, rol_id: int):
    return db.query(Rol).filter(Rol.id == rol_id).first()

def create_rol(db: Session, rol: RolCreate):
    db_rol = Rol(nombre=rol.nombre, descripcion=rol.descripcion)
    db.add(db_rol)
    db.commit()
    db.refresh(db_rol)
    return db_rol

def update_rol(db: Session, rol_id: int, rol: RolUpdate):
    db_rol = get_rol(db, rol_id)
    if not db_rol:
        return None
    if rol.nombre is not None:
        db_rol.nombre = rol.nombre
    if rol.descripcion is not None:
        db_rol.descripcion = rol.descripcion
    db.commit()
    db.refresh(db_rol)
    return db_rol

def delete_rol(db: Session, rol_id: int):
    db_rol = get_rol(db, rol_id)
    if not db_rol:
        return None
    db.delete(db_rol)
    db.commit()
    return db_rol