from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class FacultadBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class FacultadCreate(FacultadBase):
    pass

class FacultadUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None

class FacultadOut(FacultadBase):
    id: int
    fecha_creacion: datetime

    class Config:
        orm_mode = True