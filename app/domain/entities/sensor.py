from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional, List

# Tipos de sensores disponibles
SENSOR_TYPES = {
    "YL-69": "Sensor de Humedad del Sustrato",
    "DHT22": "Sensor de Temperatura y Humedad Ambiental", 
    "BH1750": "Sensor de Luz (Lux)",
    "HC-SR04": "Sensor de Nivel de Agua (Ultrasonido)",
    "YL-83": "Sensor de Lluvia",
    "SW-420": "Sensor de Vibraciones"
}

SENSOR_UNITS = {
    "YL-69": "%",
    "DHT22_TEMP": "°C",
    "DHT22_HUM": "%",
    "BH1750": "lux",
    "HC-SR04": "cm",
    "YL-83": "boolean",
    "SW-420": "boolean"
}

class SensorResponse(BaseModel):
    id_sensor: int
    tipo_sensor: str
    unidad_medida: str
    descripcion: Optional[str] = None
    id_dispositivo: int
    
    class Config:
        from_attributes = True

class SensorDetailResponse(SensorResponse):
    dispositivo_info: Optional[dict] = None
    total_lecturas: int = 0
    ultima_lectura: Optional[datetime] = None
    promedio_24h: Optional[float] = None

class SensorListResponse(BaseModel):
    sensores: List[SensorResponse]
    dispositivo_id: int
    total_sensores: int

class ReadingResponse(BaseModel):
    id_lectura: int
    valor: float
    fecha_hora: datetime
    id_sensor: int
    # Información adicional del sensor
    tipo_sensor: str
    unidad_medida: str
    
    class Config:
        from_attributes = True

class ReadingCreateRequest(BaseModel):
    id_sensor: int
    valor: float
    
    @validator('id_sensor')
    def validate_sensor_id(cls, v):
        if v <= 0:
            raise ValueError('ID del sensor debe ser positivo')
        return v

class ReadingCreateResponse(BaseModel):
    msg: str
    lectura: ReadingResponse

class ReadingListResponse(BaseModel):
    lecturas: List[ReadingResponse]
    sensor_id: int
    total: int
    skip: int
    limit: int
    date_range: Optional[dict] = None

class DeviceReadingsResponse(BaseModel):
    lecturas: List[ReadingResponse]
    dispositivo_id: int
    total: int
    skip: int
    limit: int
    sensores_incluidos: List[str]
    date_range: Optional[dict] = None

class LatestReadingsResponse(BaseModel):
    dispositivo_id: int
    ultima_actualizacion: datetime
    lecturas_por_sensor: List[dict]  # [{sensor_info, ultima_lectura, valor}]

class SensorStatsResponse(BaseModel):
    sensor_id: int
    tipo_sensor: str
    total_lecturas: int
    valor_promedio: Optional[float] = None
    valor_minimo: Optional[float] = None
    valor_maximo: Optional[float] = None
    ultima_lectura: Optional[datetime] = None
    periodo_analizado: str  # "últimas 24 horas", etc.