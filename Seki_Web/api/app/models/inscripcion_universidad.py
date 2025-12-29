from sqlalchemy import Column, Integer, ForeignKey
from app.core.database import Base
from sqlalchemy.orm import relationship

class InscripcionUniversidad(Base):
    __tablename__ = "inscripcion_universidad"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    inscripcion_id = Column(Integer, ForeignKey("inscripciones.id", ondelete="CASCADE"), nullable=False)
    universidad_id = Column(Integer, ForeignKey("universidades.id", ondelete="CASCADE"), nullable=False)

    # Relaciones
    inscripcion = relationship("Inscripcion", back_populates="inscripciones_universidad")
    universidad = relationship("Universidad", back_populates="inscripciones_universidad")