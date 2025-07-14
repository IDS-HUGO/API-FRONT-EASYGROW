from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    nombre_completo: str
    telefono: str
    correo: EmailStr
    usuario: str
    contrasena: str

class UserLogin(BaseModel):
    usuario: str
    contrasena: str
