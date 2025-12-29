from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.curso import CursoCreate, CursoUpdate, CursoResponse
from app.services import curso as curso_service
from app.core.database import get_db

router = APIRouter(prefix="/api/cursos", tags=["Cursos"])

@router.get("/", response_model=list[CursoResponse])
def get_all(db: Session = Depends(get_db)):
    return curso_service.get_cursos(db)

@router.get("/{curso_id}", response_model=CursoResponse)
def get_one(curso_id: int, db: Session = Depends(get_db)):
    curso = curso_service.get_curso(db, curso_id)
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return curso

@router.post("/", response_model=CursoResponse)
def create(curso_in: CursoCreate, db: Session = Depends(get_db)):
    return curso_service.create_curso(db, curso_in)

@router.put("/{curso_id}", response_model=CursoResponse)
def update(curso_id: int, curso_in: CursoUpdate, db: Session = Depends(get_db)):
    curso = curso_service.update_curso(db, curso_id, curso_in)
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return curso

@router.delete("/{curso_id}")
def delete(curso_id: int, db: Session = Depends(get_db)):
    curso = curso_service.delete_curso(db, curso_id)
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return {"message": "Curso eliminado correctamente"}