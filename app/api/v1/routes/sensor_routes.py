from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime, date
from typing import Optional
from app.domain.entities.sensor import (
    SensorListResponse, SensorDetailResponse, 
    ReadingListResponse, ReadingCreateRequest
)
from app.infrastructure.database.db import SessionLocal
from app.services.sensor_service import (
    get_device_sensors_service, get_sensor_detail_service,
    get_sensor_readings_service, get_device_readings_service,
    create_reading_service, get_latest_readings_service
)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/device/{device_id}", response_model=SensorListResponse)
def get_device_sensors(
    device_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener todos los sensores de un dispositivo específico
    
    - **device_id**: ID del dispositivo
    """
    try:
        result = get_device_sensors_service(db, device_id)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener sensores: {str(e)}")

@router.get("/{sensor_id}/detail", response_model=SensorDetailResponse)
def get_sensor_detail(
    sensor_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener detalles de un sensor específico
    
    - **sensor_id**: ID del sensor
    """
    try:
        result = get_sensor_detail_service(db, sensor_id)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener sensor: {str(e)}")

@router.get("/{sensor_id}/readings", response_model=ReadingListResponse)
def get_sensor_readings(
    sensor_id: int,
    skip: int = Query(0, ge=0, description="Número de lecturas a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Límite de lecturas por página"),
    date_from: Optional[datetime] = Query(None, description="Fecha inicio (YYYY-MM-DD HH:MM:SS)"),
    date_to: Optional[datetime] = Query(None, description="Fecha fin (YYYY-MM-DD HH:MM:SS)"),
    db: Session = Depends(get_db)
):
    """
    Obtener lecturas de un sensor específico con filtros de fecha
    
    - **sensor_id**: ID del sensor
    - **skip**: Número de lecturas a omitir (paginación)
    - **limit**: Límite de lecturas por página (máximo 1000)
    - **date_from**: Fecha de inicio para filtrar lecturas
    - **date_to**: Fecha de fin para filtrar lecturas
    """
    try:
        result = get_sensor_readings_service(db, sensor_id, skip, limit, date_from, date_to)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener lecturas: {str(e)}")

@router.get("/device/{device_id}/readings")
def get_device_all_readings(
    device_id: int,
    skip: int = Query(0, ge=0, description="Número de lecturas a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Límite de lecturas por página"),
    date_from: Optional[datetime] = Query(None, description="Fecha inicio"),
    date_to: Optional[datetime] = Query(None, description="Fecha fin"),
    sensor_type: Optional[str] = Query(None, description="Filtrar por tipo de sensor"),
    db: Session = Depends(get_db)
):
    """
    Obtener todas las lecturas de todos los sensores de un dispositivo
    
    - **device_id**: ID del dispositivo
    - **skip**: Número de lecturas a omitir
    - **limit**: Límite de lecturas por página
    - **date_from**: Fecha de inicio para filtrar
    - **date_to**: Fecha de fin para filtrar
    - **sensor_type**: Filtrar por tipo específico de sensor (YL-69, DHT22, BH1750, etc.)
    """
    try:
        result = get_device_readings_service(db, device_id, skip, limit, date_from, date_to, sensor_type)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener lecturas del dispositivo: {str(e)}")

@router.get("/device/{device_id}/latest")
def get_device_latest_readings(
    device_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener las últimas lecturas de cada sensor del dispositivo
    
    - **device_id**: ID del dispositivo
    """
    try:
        result = get_latest_readings_service(db, device_id)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener últimas lecturas: {str(e)}")

@router.post("/readings")
def create_sensor_reading(
    reading: ReadingCreateRequest,
    db: Session = Depends(get_db)
):
    """
    Crear una nueva lectura de sensor (generalmente usado por los dispositivos IoT)
    
    Body JSON:
    {
        "id_sensor": 1,
        "valor": 23.5
    }
    
    - **id_sensor**: ID del sensor que envía la lectura
    - **valor**: Valor medido por el sensor
    """
    try:
        result = create_reading_service(db, reading)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear lectura: {str(e)}")

# Endpoints específicos por tipo de sensor
@router.get("/device/{device_id}/humidity")
def get_device_humidity_readings(
    device_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    hours: int = Query(24, ge=1, le=168, description="Últimas X horas (máximo 7 días)"),
    db: Session = Depends(get_db)
):
    """
    Obtener lecturas de humedad del sustrato (YL-69) de las últimas X horas
    
    - **device_id**: ID del dispositivo
    - **hours**: Número de horas hacia atrás (máximo 168 = 7 días)
    """
    try:
        from app.services.sensor_service import get_device_sensor_readings_by_type_service
        result = get_device_sensor_readings_by_type_service(db, device_id, "YL-69", skip, limit, hours)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener lecturas de humedad: {str(e)}")

@router.get("/device/{device_id}/environment")
def get_device_environmental_readings(
    device_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    hours: int = Query(24, ge=1, le=168),
    db: Session = Depends(get_db)
):
    """
    Obtener lecturas ambientales (DHT22: temperatura y humedad ambiental)
    
    - **device_id**: ID del dispositivo
    - **hours**: Número de horas hacia atrás
    """
    try:
        from app.services.sensor_service import get_device_sensor_readings_by_type_service
        result = get_device_sensor_readings_by_type_service(db, device_id, "DHT22", skip, limit, hours)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener lecturas ambientales: {str(e)}")

@router.get("/device/{device_id}/light")
def get_device_light_readings(
    device_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    hours: int = Query(24, ge=1, le=168),
    db: Session = Depends(get_db)
):
    """
    Obtener lecturas de luz (BH1750) en lux
    
    - **device_id**: ID del dispositivo
    - **hours**: Número de horas hacia atrás
    """
    try:
        from app.services.sensor_service import get_device_sensor_readings_by_type_service
        result = get_device_sensor_readings_by_type_service(db, device_id, "BH1750", skip, limit, hours)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener lecturas de luz: {str(e)}")

@router.get("/device/{device_id}/water-level")
def get_device_water_level_readings(
    device_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    hours: int = Query(24, ge=1, le=168),
    db: Session = Depends(get_db)
):
    """
    Obtener lecturas del nivel de agua (HC-SR04)
    
    - **device_id**: ID del dispositivo
    - **hours**: Número de horas hacia atrás
    """
    try:
        from app.services.sensor_service import get_device_sensor_readings_by_type_service
        result = get_device_sensor_readings_by_type_service(db, device_id, "HC-SR04", skip, limit, hours)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener lecturas de nivel de agua: {str(e)}")