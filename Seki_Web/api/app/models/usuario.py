from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, text
from sqlalchemy.orm import relationship
from app.core.database import Base\


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    contrasena = Column(String(255), nullable=False)   # ← corregido
    rol = Column(String(50), nullable=False)
    fecha_creacion = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    rol_id = Column(Integer, ForeignKey("roles.id"))
    rol_rel = relationship("Rol", back_populates="usuarios")
    cursos = relationship("Curso", back_populates="profesor", cascade="all, delete-orphan")
    inscripciones = relationship("Inscripcion", back_populates="usuario")
    comentarios = relationship("Comentario", back_populates="usuario", cascade="all, delete-orphan")
    inscripciones_plataforma = relationship("InscripcionPlataforma", back_populates="usuario")