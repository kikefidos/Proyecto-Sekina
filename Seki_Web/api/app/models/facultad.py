from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Facultad(Base):
    __tablename__ = "facultades"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    descripcion = Column(Text, nullable=True)
    fecha_creacion = Column(TIMESTAMP, server_default=func.now())

    # Relación con cursos (porque tu tabla cursos tiene facultad_id)
    cursos = relationship("Curso", back_populates="facultad")