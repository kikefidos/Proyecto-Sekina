from sqlalchemy.orm import Session
from app.models.inscripcion import Inscripcion
from app.models.universidad import Universidad
from app.schemas.inscripcion import InscripcionCreate, InscripcionUpdate

def _serialize_inscripcion(ins: Inscripcion) -> dict:
    return {
        "id": ins.id,
        "usuario_id": ins.usuario_id,
        "curso_id": ins.curso_id,
        "nombre_estudiante": ins.nombre_estudiante,
        "contacto_estudiante": ins.contacto_estudiante,
        "nombre_representante": ins.nombre_representante,
        "contacto_representante": ins.contacto_representante,
        "carrera_id": ins.carrera_id,
        "metodo_pago": ins.metodo_pago,
        "valor_pago": float(ins.valor_pago) if ins.valor_pago is not None else None,
        "cuotas": ins.cuotas,
        "horarios": ins.horarios,
        "dias": ins.dias,
        "regimen_id": ins.regimen_id,
        "fecha_inscripcion": ins.fecha_inscripcion,
        "fecha_pago": ins.fecha_pago,
        "progreso": float(ins.progreso) if ins.progreso is not None else 0.0,
        "universidades": [u.id for u in getattr(ins, "universidades", [])]
    }

def get_inscripciones(db: Session, skip: int = 0, limit: int = 100):
    rows = db.query(Inscripcion).offset(skip).limit(limit).all()
    return [_serialize_inscripcion(r) for r in rows]

def get_inscripcion(db: Session, inscripcion_id: int):
    ins = db.query(Inscripcion).filter(Inscripcion.id == inscripcion_id).first()
    return _serialize_inscripcion(ins) if ins else None

def create_inscripcion(db: Session, inscripcion: InscripcionCreate):
    data = inscripcion.dict(exclude={"universidades"})
    if data.get("regimen_id") is None:
        data["regimen_id"] = 1

    db_inscripcion = Inscripcion(**data)

    if inscripcion.universidades:
        universidades = db.query(Universidad).filter(Universidad.id.in_(inscripcion.universidades)).all()
        db_inscripcion.universidades = universidades

    db.add(db_inscripcion)
    db.commit()
    db.refresh(db_inscripcion)
    return _serialize_inscripcion(db_inscripcion)

def update_inscripcion(db: Session, inscripcion_id: int, inscripcion: InscripcionUpdate):
    db_inscripcion = db.query(Inscripcion).filter(Inscripcion.id == inscripcion_id).first()
    if not db_inscripcion:
        return None

    for key, value in inscripcion.dict(exclude_unset=True, exclude={"universidades"}).items():
        setattr(db_inscripcion, key, value)

    if inscripcion.universidades is not None:
        universidades = db.query(Universidad).filter(Universidad.id.in_(inscripcion.universidades)).all()
        db_inscripcion.universidades = universidades

    db.commit()
    db.refresh(db_inscripcion)
    return _serialize_inscripcion(db_inscripcion)

def delete_inscripcion(db: Session, inscripcion_id: int):
    db_inscripcion = db.query(Inscripcion).filter(Inscripcion.id == inscripcion_id).first()
    if not db_inscripcion:
        return None
    result = _serialize_inscripcion(db_inscripcion)
    db.delete(db_inscripcion)
    db.commit()
    return result