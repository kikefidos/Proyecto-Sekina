# app/services/usuario_service.py
from sqlalchemy.orm import Session
from app import models
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate
from app.utils.hashing import Hasher
from datetime import datetime


def crear_usuario(db: Session, usuario: UsuarioCreate):
    hashed_password = Hasher.hash_password(usuario.contrasena)
    nuevo_usuario = models.Usuario(
        nombre=usuario.nombre,
        apellido=usuario.apellido,
        email=usuario.email,
        contrasena=hashed_password,
        rol_id=usuario.rol_id,
        fecha_creacion=datetime.utcnow()
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario


def actualizar_usuario(db: Session, usuario_id: int, usuario: UsuarioUpdate):
    db_usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not db_usuario:
        return None

    if usuario.nombre:
        db_usuario.nombre = usuario.nombre
    if usuario.apellido:
        db_usuario.apellido = usuario.apellido
    if usuario.email:
        db_usuario.email = usuario.email
    if usuario.contrasena:
        db_usuario.contrasena = Hasher.hash_password(usuario.contrasena)
    if usuario.rol_id:
        db_usuario.rol_id = usuario.rol_id

    db.commit()
    db.refresh(db_usuario)
    return db_usuario