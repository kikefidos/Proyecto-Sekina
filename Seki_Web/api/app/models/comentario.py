from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from app.core.database import Base

class Comentario(Base):
    __tablename__ = "comentarios"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    curso_id = Column(Integer, ForeignKey("cursos.id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    contenido = Column(Text, nullable=False)
    fecha_creacion = Column(TIMESTAMP, nullable=True)

    # Relaciones
    curso = relationship("Curso", back_populates="comentarios")
    usuario = relationship("Usuario", back_populates="comentarios")