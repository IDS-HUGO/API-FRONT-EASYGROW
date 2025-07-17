from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional
import re

class DeviceCreate(BaseModel):
    mac_address: str
    nombre_dispositivo: Optional[str] = None

    @validator('mac_address')
    def validate_mac_address(cls, v):
        # Validar formato MAC address (XX:XX:XX:XX:XX:XX)
        mac_pattern = re.compile(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$')
        if not mac_pattern.match(v):
            raise ValueError('Formato de MAC address inválido. Use formato XX:XX:XX:XX:XX:XX')
        return v.upper()  # Convertir a mayúsculas para consistencia

class DeviceAssignRequest(BaseModel):
    user_id: int
    mac_address: str
    nombre_dispositivo: Optional[str] = None

    @validator('mac_address')
    def validate_mac_address(cls, v):
        mac_pattern = re.compile(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$')
        if not mac_pattern.match(v):
            raise ValueError('Formato de MAC address inválido. Use formato XX:XX:XX:XX:XX:XX')
        return v.upper()

    @validator('user_id')
    def validate_user_id(cls, v):
        if v <= 0:
            raise ValueError('user_id debe ser mayor a 0')
        return v

class DeviceResponse(BaseModel):
    id_dispositivo: int
    mac_address: str
    nombre_dispositivo: Optional[str] = None
    fecha_asignacion: datetime
    id_usuario: int

    class Config:
        from_attributes = True

class DeviceAssignResponse(BaseModel):
    msg: str
    dispositivo: DeviceResponse