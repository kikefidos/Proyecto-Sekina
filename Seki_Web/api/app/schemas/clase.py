from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ClaseBase(BaseModel):
    curso_id: int
    titulo: str
    url_video: str
    duracion: float
    orden: int

class ClaseCreate(ClaseBase):
    pass

class ClaseUpdate(BaseModel):
    titulo: Optional[str] = None
    url_video: Optional[str] = None
    duracion: Optional[float] = None
    orden: Optional[int] = None

class ClaseOut(ClaseBase):
    id: int
    fecha_creacion: datetime

    class Config:
        orm_mode = True