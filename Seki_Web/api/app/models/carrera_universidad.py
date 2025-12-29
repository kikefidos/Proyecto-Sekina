from sqlalchemy import Table, Column, Integer, ForeignKey
from app.core.database import Base

# Tabla intermedia N:M entre carreras y universidades
carrera_universidad = Table(
    "carrera_universidad",
    Base.metadata,
    Column("carrera_id", Integer, ForeignKey("carreras.id"), primary_key=True),
    Column("universidad_id", Integer, ForeignKey("universidades.id"), primary_key=True),
)