from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Inscripcion
from schemas import ProgresoUpdate
from routers import get_current_user

router = APIRouter()

@router.post("/", summary="Actualizar progreso de un curso (0-100%)")
def actualizar_progreso(data: ProgresoUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    ins = db.query(Inscripcion).filter(
        Inscripcion.usuario_id == user.id,
        Inscripcion.curso_id == data.curso_id
    ).first()

    if not ins:
        raise HTTPException(status_code=404, detail="No estás inscrito en este curso")

    ins.progreso = float(data.progreso)
    db.commit()
    return {"ok": True, "progreso": ins.progreso}