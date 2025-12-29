from pydantic import BaseModel

class RegimenBase(BaseModel):
    nombre: str

class RegimenCreate(RegimenBase):
    pass

class RegimenResponse(RegimenBase):
    id: int

    class Config:
        orm_mode = True