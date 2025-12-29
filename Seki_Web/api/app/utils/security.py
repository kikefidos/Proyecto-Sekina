from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_contrasena_hash(contrasena: str) -> str:  # <-- cambiado
    return pwd_context.hash(contrasena)

def verify_contrasena(plain_contrasena: str, hashed_contrasena: str) -> bool:  # <-- cambiado
    return pwd_context.verify(plain_contrasena, hashed_contrasena)




