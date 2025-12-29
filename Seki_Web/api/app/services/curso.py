from sqlalchemy.orm import Session
from app.models.curso import Curso
from app.schemas.curso import CursoCreate, CursoUpdate

def get_cursos(db: Session):
    return db.query(Curso).all()

def get_curso(db: Session, curso_id: int):
    return db.query(Curso).filter(Curso.id == curso_id).first()

def create_curso(db: Session, curso_in: CursoCreate):
    curso = Curso(**curso_in.dict())
    db.add(curso)
    db.commit()
    db.refresh(curso)
    return curso

def update_curso(db: Session, curso_id: int, curso_in: CursoUpdate):
    curso = get_curso(db, curso_id)
    if not curso:
        return None
    for key, value in curso_in.dict().items():
        setattr(curso, key, value)
    db.commit()
    db.refresh(curso)
    return curso

def delete_curso(db: Session, curso_id: int):
    curso = get_curso(db, curso_id)
    if not curso:
        return None
    db.delete(curso)
    db.commit()
    return curso