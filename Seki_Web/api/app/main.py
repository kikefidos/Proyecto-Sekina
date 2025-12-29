from app.routers import inscripcion, rol, usuario, auth,universidad,carrera,cursos, carrera_universidad,clase,facultad,inscripciones_plataforma,regimen
from fastapi import FastAPI
from app.core.database import Base, engine

# Import all models to ensure they are registered
from app.models import (
    Usuario, Rol, Universidad, Carrera, Curso, Clase, Comentario, Facultad,
    InscripcionUniversidad, Inscripcion, InscripcionPlataforma, Regimen
)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Seki API")

app.include_router(rol.router)
app.include_router(usuario.router)
app.include_router(auth.router)
app.include_router(inscripcion.router)
app.include_router(universidad.router)
app.include_router(carrera.router)
app.include_router(cursos.router)
app.include_router(clase.router)
app.include_router(carrera_universidad.router)
app.include_router(facultad.router)
app.include_router(inscripciones_plataforma.router)
app.include_router(regimen.router)

@app.get("/")
def root():
    return {"message": "API funcionando 🚀"}