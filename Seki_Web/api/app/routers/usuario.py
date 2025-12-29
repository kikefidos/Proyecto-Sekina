from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.usuario import UsuarioCreate, UsuarioResponse, UsuarioLogin,UsuarioUpdate
from passlib.context import CryptContext
from app.models.usuario import Usuario
from app.services.usuario import actualizar_usuario

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hashear contrasena
def hash_contrasena(contrasena: str) -> str:
    return pwd_context.hash(contrasena)

# Verificar contrasena
def verify_contrasena(plain_contrasena: str, hashed_contrasena: str) -> bool:
    return pwd_context.verify(plain_contrasena, hashed_contrasena)

# Registro
@router.post("/registro", response_model=UsuarioResponse)
def registrar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    usuario_existente = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    nuevo_usuario = Usuario(
        nombre=usuario.nombre,
        apellido=getattr(usuario, "apellido", None),
        email=usuario.email,
        contrasena=hash_contrasena(usuario.contrasena),  # <-- cambiado
        rol_id=usuario.rol_id
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

@router.put("/{usuario_id}", response_model=UsuarioResponse)
def modificar_usuario(usuario_id: int, usuario: UsuarioUpdate, db: Session = Depends(get_db)):
    db_usuario = actualizar_usuario(db, usuario_id, usuario)
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario

# Login
@router.post("/login")
def login(usuario: UsuarioLogin, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if not user or not verify_contrasena(usuario.contrasena, user.contrasena):  # <-- cambiado
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    return {"message": f"Bienvenido {user.nombre}", "usuario_id": user.id, "rol_id": user.rol_id}