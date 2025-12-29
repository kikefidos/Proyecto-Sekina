from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class NivelEnum(str, Enum):
    Basico = "Basico"
    Intermedio = "Intermedio"
    Avanzado = "Avanzado"

class CursoBase(BaseModel):
    titulo: str
    facultad_id: int
    nivel: NivelEnum
    clases: int
    horas: float
    descripcion: Optional[str] = None
    profesor_id: int

class CursoCreate(CursoBase):
    pass

class CursoUpdate(BaseModel):
    titulo: Optional[str] = None
    facultad_id: Optional[int] = None
    nivel: Optional[NivelEnum] = None
    clases: Optional[int] = None
    horas: Optional[float] = None
    descripcion: Optional[str] = None
    profesor_id: Optional[int] = None

class CursoResponse(CursoBase):
    id: int
    fecha_creacion: Optional[datetime] = None

    class Config:
        from_attributes = True