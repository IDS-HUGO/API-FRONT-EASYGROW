# app/domain/entities/plant.py - Parte actualizada

from pydantic import BaseModel, validator
from datetime import datetime, date
from typing import Optional, List

class PlantCreateRequest(BaseModel):
    id_catalogo: int
    id_usuario: int
    id_dispositivo: Optional[int] = None
    nombre_personalizado: Optional[str] = None
    ubicacion: Optional[str] = None
    fecha_plantacion: Optional[date] = None
    notas_usuario: Optional[str] = None

    @validator('id_catalogo', 'id_usuario')
    def validate_positive_ids(cls, v):
        if v <= 0:
            raise ValueError('Los IDs deben ser números positivos')
        return v

    @validator('id_dispositivo')
    def validate_device_id(cls, v):
        if v is not None and v <= 0:
            raise ValueError('El ID del dispositivo debe ser un número positivo')
        return v

    @validator('nombre_personalizado')
    def validate_custom_name(cls, v):
        if v is not None and len(v.strip()) == 0:
            raise ValueError('El nombre personalizado no puede estar vacío')
        return v.strip() if v else v

    @validator('ubicacion')
    def validate_location(cls, v):
        if v is not None and len(v.strip()) == 0:
            raise ValueError('La ubicación no puede estar vacía')
        return v.strip() if v else v

class CatalogPlantInfo(BaseModel):
    id_catalogo: int
    nombre_comun: str
    nombre_cientifico: str
    descripcion: Optional[str] = None
    altura_maxima_cm: Optional[int] = None
    cuidados_especiales: Optional[str] = None
    imagen_referencia: Optional[str] = None  # ✅ AGREGADO
    
    class Config:
        from_attributes = True

class PlantResponse(BaseModel):
    id_planta: int
    id_catalogo: int
    id_usuario: int
    id_dispositivo: Optional[int] = None
    nombre_personalizado: Optional[str] = None
    ubicacion: Optional[str] = None
    fecha_plantacion: Optional[date] = None
    fecha_registro: datetime
    notas_usuario: Optional[str] = None
    activa: bool
    # Información del catálogo
    catalogo_info: CatalogPlantInfo
    
    class Config:
        from_attributes = True

class PlantCreateResponse(BaseModel):
    msg: str
    planta: PlantResponse

class UserPlantsResponse(BaseModel):
    user_id: int
    plantas: List[PlantResponse]
    total_plantas: int
    plantas_activas: int
    plantas_con_dispositivo: int

class DevicePlantsResponse(BaseModel):
    device_id: int
    mac_address: str
    nombre_dispositivo: Optional[str] = None
    plantas: List[PlantResponse]
    total_plantas: int

class UserDevicePlantsResponse(BaseModel):
    user_id: int
    device_id: int
    plantas: List[PlantResponse]
    total_plantas: int

class PlantDetailResponse(PlantResponse):
    # Información extendida
    dias_desde_plantacion: Optional[int] = None
    dispositivo_info: Optional[dict] = None
    ultimas_lecturas: Optional[List[dict]] = None
    estadisticas_sensores: Optional[dict] = None
    
class PlantDeleteResponse(BaseModel):
    msg: str
    plant_id: int
    deleted_permanently: bool = False