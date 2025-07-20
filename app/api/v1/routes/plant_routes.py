from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.domain.entities.plant import PlantCreateRequest, PlantCreateResponse
from app.infrastructure.database.db import SessionLocal
from app.services.plant_service import create_plant_service

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=PlantCreateResponse)
def create_plant(
    plant_request: PlantCreateRequest, 
    db: Session = Depends(get_db)
):
    """
    Crear una nueva planta asociada a un usuario y dispositivo
    
    Body JSON:
    {
        "id_catalogo": 1,
        "id_usuario": 1,
        "id_dispositivo": 1,
        "nombre_personalizado": "Mi Albahaca del Jardín",
        "ubicacion": "Ventana de la cocina",
        "fecha_plantacion": "2025-01-15",
        "notas_usuario": "Primera planta en mi huerto urbano"
    }
    
    - **id_catalogo**: ID de la planta del catálogo (obligatorio)
    - **id_usuario**: ID del usuario propietario (obligatorio)
    - **id_dispositivo**: ID del dispositivo de monitoreo (opcional)
    - **nombre_personalizado**: Nombre personalizado para la planta
    - **ubicacion**: Ubicación física de la planta
    - **fecha_plantacion**: Fecha cuando se plantó (formato YYYY-MM-DD)
    - **notas_usuario**: Notas adicionales del usuario
    """
    try:
        result = create_plant_service(db, plant_request)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
@router.get("/user/{user_id}")
def get_user_plants(
    user_id: int,
    active_only: bool = Query(True, description="Solo plantas activas"),
    db: Session = Depends(get_db)
):
    """
    Obtener todas las plantas de un usuario específico
    
    - **user_id**: ID del usuario
    - **active_only**: Solo mostrar plantas activas (por defecto True)
    """
    try:
        from app.services.plant_service import get_user_plants_service
        result = get_user_plants_service(db, user_id, active_only)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener plantas del usuario: {str(e)}")

@router.get("/device/{device_id}")
def get_device_plants(
    device_id: int,
    active_only: bool = Query(True, description="Solo plantas activas"),
    db: Session = Depends(get_db)
):
    """
    Obtener todas las plantas monitoreadas por un dispositivo específico
    
    - **device_id**: ID del dispositivo
    - **active_only**: Solo mostrar plants activas (por defecto True)
    """
    try:
        from app.services.plant_service import get_device_plants_service
        result = get_device_plants_service(db, device_id, active_only)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener plantas del dispositivo: {str(e)}")

@router.get("/user/{user_id}/device/{device_id}")
def get_user_device_plants(
    user_id: int,
    device_id: int,
    active_only: bool = Query(True, description="Solo plantas activas"),
    db: Session = Depends(get_db)
):
    """
    Obtener plantas de un usuario específico monitoreadas por un dispositivo específico
    
    - **user_id**: ID del usuario
    - **device_id**: ID del dispositivo
    - **active_only**: Solo mostrar plantas activas (por defecto True)
    """
    try:
        from app.services.plant_service import get_user_device_plants_service
        result = get_user_device_plants_service(db, user_id, device_id, active_only)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener plantas: {str(e)}")

@router.get("/{plant_id}/detail")
def get_plant_detail(
    plant_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener detalles completos de una planta específica
    
    - **plant_id**: ID de la planta
    """
    try:
        from app.services.plant_service import get_plant_detail_service
        result = get_plant_detail_service(db, plant_id)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener detalle de la planta: {str(e)}")