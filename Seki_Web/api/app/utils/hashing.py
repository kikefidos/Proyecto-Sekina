from passlib.context import CryptContext

# Configuración de Passlib con bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hasher:
    @staticmethod
    def verificar_password(password: str, hashed_password: str) -> bool:
        """
        Verifica que la contraseña en texto plano coincida con la hasheada
        """
        return pwd_context.verify(password, hashed_password)

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Genera el hash de una contraseña
        """
        return pwd_context.hash(password)