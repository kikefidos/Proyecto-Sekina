from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional, List

class InscripcionBase(BaseModel):
    usuario_id: int
    curso_id: int
    nombre_estudiante: str
    contacto_estudiante: str
    nombre_representante: str
    contacto_representante: str
    carrera_id: int
    metodo_pago: str
    valor_pago: float
    cuotas: int
    horarios: Optional[str] = None
    dias: Optional[str] = None

    regimen_id: Optional[int] = 1

class InscripcionCreate(InscripcionBase):
    universidades: Optional[List[int]] = []  # lista de IDs de universidades

class InscripcionUpdate(BaseModel):
    progreso: Optional[float] = None
    metodo_pago: Optional[str] = None
    valor_pago: Optional[float] = None
    cuotas: Optional[int] = None
    horarios: Optional[str] = None
    dias: Optional[str] = None
    universidades: Optional[List[int]] = None
    regimen_id: Optional[int] = None

class InscripcionOut(InscripcionBase):
    id: int
    fecha_inscripcion: datetime
    fecha_pago: date
    progreso: float
    universidades: List[int] = []  # devolver solo IDs de universidades

    class Config:
        from_attributes = True