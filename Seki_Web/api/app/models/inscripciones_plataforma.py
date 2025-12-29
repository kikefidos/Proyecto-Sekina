from sqlalchemy import Column, Integer, ForeignKey, DECIMAL, TIMESTAMP, text
from sqlalchemy.orm import relationship
from app.core.database import Base

class InscripcionPlataforma(Base):
    __tablename__ = "inscripciones_plataforma"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    curso_id = Column(Integer, ForeignKey("cursos.id"), nullable=False)
    fecha_inscripcion = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    progreso = Column(DECIMAL(5,2), server_default="0.00")

    # Relaciones
    usuario = relationship("Usuario", back_populates="inscripciones_plataforma")
    curso = relationship("Curso", back_populates="inscripciones_plataforma")