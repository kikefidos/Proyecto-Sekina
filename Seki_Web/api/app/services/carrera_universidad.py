from sqlalchemy.orm import Session
from app.models.carrera import Carrera
from app.models.universidad import Universidad
from app.models.carrera_universidad import carrera_universidad

# Crear relación
def create_relacion(db: Session, carrera_id: int, universidad_id: int):
    carrera = db.query(Carrera).get(carrera_id)
    universidad = db.query(Universidad).get(universidad_id)
    if not carrera or not universidad:
        return None
    
    carrera.universidades.append(universidad)
    db.commit()
    db.refresh(carrera)
    return {"carrera_id": carrera_id, "universidad_id": universidad_id}

# Listar universidades de una carrera
def get_universidades_by_carrera(db: Session, carrera_id: int):
    carrera = db.query(Carrera).get(carrera_id)
    if not carrera:
        return None
    return carrera.universidades

# Listar carreras de una universidad
def get_carreras_by_universidad(db: Session, universidad_id: int):
    universidad = db.query(Universidad).get(universidad_id)
    if not universidad:
        return None
    return universidad.carreras

# Eliminar relación
def delete_relacion(db: Session, carrera_id: int, universidad_id: int):
    carrera = db.query(Carrera).get(carrera_id)
    universidad = db.query(Universidad).get(universidad_id)
    if not carrera or not universidad:
        return None
    
    if universidad in carrera.universidades:
        carrera.universidades.remove(universidad)
        db.commit()
        return True
    return False