from sqlalchemy import Column, Integer, String, Text, Enum, DECIMAL, ForeignKey, TIMESTAMP, text
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum

class NivelEnum(enum.Enum):
    Basico = "Basico"
    Intermedio = "Intermedio"
    Avanzado = "Avanzado"

class Curso(Base):
    __tablename__ = "cursos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    titulo = Column(String(255), nullable=False)
    facultad_id = Column(Integer, ForeignKey("facultades.id"), nullable=False)
    nivel = Column(Enum(NivelEnum), nullable=False)
    clases = Column(Integer, nullable=False) 
    horas = Column(DECIMAL(5, 2), nullable=False)
    descripcion = Column(Text, nullable=True)
    profesor_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    fecha_creacion = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))

    # Relaciones
    facultad = relationship("Facultad", back_populates="cursos")
    profesor = relationship("Usuario", back_populates="cursos")
    clasesr = relationship("Clase", back_populates="curso", cascade="all, delete-orphan")
    inscripciones = relationship("Inscripcion", back_populates="curso")
    inscripciones_plataforma = relationship("InscripcionPlataforma", back_populates="curso")
    comentarios = relationship("Comentario", back_populates="curso", cascade="all, delete-orphan")