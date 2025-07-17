from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

class UserCreate(BaseModel):
    nombre_completo: str
    telefono: str
    correo: EmailStr
    usuario: str
    contrasena: str

class UserLogin(BaseModel):
    usuario: str
    contrasena: str

class DispositivoResponse(BaseModel):
    id_dispositivo: int
    mac_address: str
    nombre_dispositivo: Optional[str] = None
    fecha_asignacion: datetime
    
    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    id_usuario: int
    nombre_completo: str
    telefono: Optional[str] = None
    correo: str
    usuario: str
    fecha_registro: datetime
    dispositivos: List[DispositivoResponse] = []
    
    class Config:
        from_attributes = True

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user_info: UserResponse

class UsersListResponse(BaseModel):
    usuarios: List[UserResponse]
    total: int
    skip: int
    limit: int