from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.carrera_universidad import carrera_universidad

class Carrera(Base):
    __tablename__ = "carreras"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)

    universidades = relationship(
        "Universidad",
        secondary=carrera_universidad,
        back_populates="carreras"
    )