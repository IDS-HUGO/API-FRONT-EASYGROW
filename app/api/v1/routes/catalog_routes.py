from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.domain.entities.catalog import CatalogListResponse, CatalogPlantDetailResponse
from app.infrastructure.database.db import SessionLocal
from app.services.catalog_service import get_all_catalog_plants_service, get_catalog_plant_by_id_service

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=CatalogListResponse)
def get_catalog_plants(
    skip: int = Query(0, ge=0, description="Número de plantas a omitir"),
    limit: int = Query(50, ge=1, le=100, description="Límite de plantas por página"),
    search: str = Query(None, description="Buscar por nombre común o científico"),
    active_only: bool = Query(True, description="Solo plantas activas"),
    db: Session = Depends(get_db)
):
    """
    Obtener todas las plantas del catálogo con paginación y filtros
    
    - **skip**: Número de plantas a omitir (para paginación)
    - **limit**: Límite de plantas por página (máximo 100)
    - **search**: Búsqueda por nombre común o científico (opcional)
    - **active_only**: Solo mostrar plantas activas (por defecto True)
    """
    try:
        result = get_all_catalog_plants_service(db, skip, limit, search, active_only)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.get("/{catalog_id}", response_model=CatalogPlantDetailResponse)
def get_catalog_plant_detail(
    catalog_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener detalles específicos de una planta del catálogo
    
    - **catalog_id**: ID de la planta en el catálogo
    """
    try:
        result = get_catalog_plant_by_id_service(db, catalog_id)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")