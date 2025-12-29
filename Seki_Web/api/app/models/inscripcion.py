from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey, TIMESTAMP, Date, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Inscripcion(Base):
    __tablename__ = "inscripciones"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    curso_id = Column(Integer, ForeignKey("cursos.id"), nullable=False)
    fecha_inscripcion = Column(TIMESTAMP, server_default=func.now())
    progreso = Column(DECIMAL(5,2), default=0.00)

    nombre_estudiante = Column(String(255), nullable=False)
    contacto_estudiante = Column(String(50), nullable=False)
    nombre_representante = Column(String(255), nullable=False)
    contacto_representante = Column(String(50), nullable=False)

    horarios = Column(String(50), nullable=True)
    dias = Column(String(20), nullable=True)

    carrera_id = Column(Integer, ForeignKey("carreras.id"), nullable=False)

    metodo_pago = Column(String(50), nullable=False)
    valor_pago = Column(DECIMAL(10,2), nullable=False)
    fecha_pago = Column(Date, server_default=func.current_date())
    cuotas = Column(Integer, default=1)

    # reemplazamos `region` por foreign key a regimen
    regimen_id = Column(Integer, ForeignKey("regimen.id"), nullable=False, default=1)

    # Relaciones
    usuario = relationship("Usuario", back_populates="inscripciones")
    curso = relationship("Curso", back_populates="inscripciones")
    universidades = relationship("Universidad", secondary="inscripcion_universidad", back_populates="inscripciones")
    regimen = relationship("Regimen")

    # Relación con la tabla intermedia
    inscripciones_universidad = relationship(
        "InscripcionUniversidad",
        back_populates="inscripcion",
        cascade="all, delete-orphan"
    )