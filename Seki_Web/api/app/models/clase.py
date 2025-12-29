from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, TIMESTAMP, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Clase(Base):
    __tablename__ = "clases"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    curso_id = Column(Integer, ForeignKey("cursos.id"), nullable=False)
    titulo = Column(String(255), nullable=False)
    url_video = Column(String(500), nullable=False)
    duracion = Column(DECIMAL(5, 2), nullable=False)
    orden = Column(Integer, nullable=False)
    fecha_creacion = Column(TIMESTAMP, server_default=func.now())

    # relación con Curso
    curso = relationship("Curso", back_populates="clasesr")