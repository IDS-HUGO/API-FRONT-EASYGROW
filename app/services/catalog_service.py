from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.domain.repositories.catalog_repository import (
    get_all_catalog_plants,
    get_catalog_plant_by_id_with_stats,
    count_catalog_plants
)
from app.domain.entities.catalog import (
    CatalogListResponse, 
    CatalogPlantDetailResponse,
    CatalogPlantBasic
)

def get_all_catalog_plants_service(
    db: Session, 
    skip: int = 0, 
    limit: int = 50, 
    search: Optional[str] = None, 
    active_only: bool = True
):
    """Obtener todas las plantas del catálogo con filtros y paginación"""
    try:
        # Obtener plantas del repositorio
        plants = get_all_catalog_plants(db, skip, limit, search, active_only)
        
        # Contar total de plantas
        total = count_catalog_plants(db, search, active_only)
        
        # Convertir a formato de respuesta
        catalog_plants = [
            CatalogPlantBasic(
                id_catalogo=plant.id_catalogo,
                nombre_comun=plant.nombre_comun,
                nombre_cientifico=plant.nombre_cientifico,
                descripcion=plant.descripcion,
                altura_maxima_cm=plant.altura_maxima_cm,
                imagen_referencia=plant.imagen_referencia,
                activo=plant.activo
            )
            for plant in plants
        ]
        
        return CatalogListResponse(
            plantas=catalog_plants,
            total=total,
            skip=skip,
            limit=limit,
            search_term=search
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error al obtener plantas del catálogo: {str(e)}"
        )

def get_catalog_plant_by_id_service(db: Session, catalog_id: int):
    """Obtener detalles específicos de una planta del catálogo"""
    try:
        # Obtener planta con estadísticas
        plant_data = get_catalog_plant_by_id_with_stats(db, catalog_id)
        
        if not plant_data:
            raise HTTPException(
                status_code=404, 
                detail="Planta no encontrada en el catálogo"
            )
        
        plant, stats = plant_data
        
        return CatalogPlantDetailResponse(
            id_catalogo=plant.id_catalogo,
            nombre_comun=plant.nombre_comun,
            nombre_cientifico=plant.nombre_cientifico,
            descripcion=plant.descripcion,
            altura_maxima_cm=plant.altura_maxima_cm,
            imagen_referencia=plant.imagen_referencia,
            activo=plant.activo,
            cuidados_especiales=plant.cuidados_especiales,
            fecha_creacion=plant.fecha_creacion,
            total_plantas_registradas=stats.get('total_plantas', 0),
            usuarios_activos=stats.get('usuarios_activos', 0)
        )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error al obtener detalles de la planta: {str(e)}"
        )