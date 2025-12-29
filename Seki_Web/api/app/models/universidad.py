from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.carrera_universidad import carrera_universidad

class Universidad(Base):
    __tablename__ = "universidades"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False, unique=True)
    ubicacion = Column(String(255), nullable=True)

    carreras = relationship(
        "Carrera",
        secondary=carrera_universidad,
        back_populates="universidades"
    )

    # Relación con la tabla intermedia
    inscripciones_universidad = relationship(
        "InscripcionUniversidad",
        back_populates="universidad",
        cascade="all, delete-orphan"
    )

    # Relación many-to-many con inscripciones
    inscripciones = relationship(
        "Inscripcion",
        secondary="inscripcion_universidad",
        back_populates="universidades"
    )