from pydantic import BaseModel

class CarreraUniversidadBase(BaseModel):
    carrera_id: int
    universidad_id: int

class CarreraUniversidadCreate(CarreraUniversidadBase):
    pass

class CarreraUniversidadResponse(CarreraUniversidadBase):
    class Config:
        from_attributes = True