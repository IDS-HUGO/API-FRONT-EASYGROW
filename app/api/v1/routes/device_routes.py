from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.domain.entities.device import DeviceAssignRequest, DeviceAssignResponse
from app.infrastructure.database.db import SessionLocal
from app.services.device_service import assign_device_to_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/assign", response_model=DeviceAssignResponse)
def assign_device(
    device_request: DeviceAssignRequest, 
    db: Session = Depends(get_db)
):
    """
    Asignar un dispositivo (MAC address) a un usuario
    
    Body JSON:
    {
        "user_id": 1,
        "mac_address": "AA:BB:CC:DD:EE:FF",
        "nombre_dispositivo": "Mi Sensor de Jardín"
    }
    
    - **user_id**: ID del usuario al que se asignará el dispositivo
    - **mac_address**: Dirección MAC del dispositivo (formato XX:XX:XX:XX:XX:XX)
    - **nombre_dispositivo**: Nombre opcional para el dispositivo
    """
    try:
        result = assign_device_to_user(db, device_request)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.get("/user/{user_id}")
def get_user_devices(user_id: int, db: Session = Depends(get_db)):
    """
    Obtener todos los dispositivos de un usuario
    
    - **user_id**: ID del usuario
    """
    from app.domain.repositories.device_repository import get_user_devices as get_devices
    
    try:
        devices = get_devices(db, user_id)
        return {
            "user_id": user_id,
            "devices": devices,
            "total_devices": len(devices)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener dispositivos: {str(e)}")