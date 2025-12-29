from pydantic import BaseModel
from typing import List, Optional

class CarreraBase(BaseModel):
    nombre: str

class CarreraCreate(CarreraBase):
    pass

class CarreraUpdate(CarreraBase):
    pass

class CarreraResponse(CarreraBase):
    id: int
    universidades: Optional[List[int]] = []  # 👈 lista de IDs de universidades

    class Config:
        from_attributes = True