from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class InscripcionPlataformaBase(BaseModel):
    usuario_id: int
    curso_id: int
    progreso: Optional[float] = 0.0

class InscripcionPlataformaCreate(InscripcionPlataformaBase):
    pass

class InscripcionPlataformaUpdate(BaseModel):
    progreso: Optional[float] = None

class InscripcionPlataformaOut(InscripcionPlataformaBase):
    id: int
    fecha_inscripcion: datetime

    class Config:
        orm_mode = True