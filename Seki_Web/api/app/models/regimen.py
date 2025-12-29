from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class Regimen(Base):
    __tablename__ = "regimen"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)

    # Relación con inscripciones
    inscripciones = relationship("Inscripcion", back_populates="regimen")