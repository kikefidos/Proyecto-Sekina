from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class UniversidadBase(BaseModel):
    nombre: str
    ubicacion: Optional[str] = None

class UniversidadCreate(UniversidadBase):
    pass

class UniversidadUpdate(UniversidadBase):
    pass

class UniversidadResponse(UniversidadBase):
    id: int
    carreras: Optional[List[int]] = []  # 👈 lista de IDs de carreras

    class Config:
        from_attributes = True