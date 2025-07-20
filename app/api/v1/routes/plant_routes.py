from fastapi import APIRouter, Depends, HTTPException
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