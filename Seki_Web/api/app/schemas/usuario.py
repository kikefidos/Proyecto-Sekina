from pydantic import BaseModel, EmailStr
from datetime import datetime 

class UsuarioBase(BaseModel):
    nombre: str
    apellido: str
    email: EmailStr
    rol_id: int

class UsuarioCreate(BaseModel):
    nombre: str
    apellido: str
    email: str
    contrasena: str
    rol_id: int  # <-- cambiado

class UsuarioUpdate(BaseModel):
    nombre: str | None = None
    apellido: str | None = None
    email: EmailStr | None = None
    rol_id: int | None = None
    contrasena: str | None = None  # <-- cambiado
    
class UsuarioLogin(BaseModel):
    email: EmailStr
    contrasena: str
    
class UsuarioResponse(BaseModel):
    id: int
    nombre: str
    apellido: str
    email: str
    rol_id: int
    fecha_creacion: datetime

    class Config:
        from_attributes = True