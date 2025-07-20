from sqlalchemy.orm import Session
from sqlalchemy import func, distinct
from app.infrastructure.database.models import CatalogoPlanta, Planta, Usuario
from typing import Optional

def get_all_catalog_plants(
    db: Session, 
    skip: int = 0, 
    limit: int = 50, 
    search: Optional[str] = None, 
    active_only: bool = True
):
    """Obtener plantas del catálogo con filtros"""
    query = db.query(CatalogoPlanta)
    
    # Filtrar solo activas si se especifica
    if active_only:
        query = query.filter(CatalogoPlanta.activo == True)
    
    # Aplicar búsqueda si se proporciona
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (CatalogoPlanta.nombre_comun.ilike(search_term)) |
            (CatalogoPlanta.nombre_cientifico.ilike(search_term))
        )
    
    # Ordenar por nombre común
    query = query.order_by(CatalogoPlanta.nombre_comun)
    
    # Aplicar paginación
    return query.offset(skip).limit(limit).all()

def count_catalog_plants(
    db: Session, 
    search: Optional[str] = None, 
    active_only: bool = True
):
    """Contar total de plantas del catálogo con filtros"""
    query = db.query(CatalogoPlanta)
    
    if active_only:
        query = query.filter(CatalogoPlanta.activo == True)
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (CatalogoPlanta.nombre_comun.ilike(search_term)) |
            (CatalogoPlanta.nombre_cientifico.ilike(search_term))
        )
    
    return query.count()

def get_catalog_plant_by_id_with_stats(db: Session, catalog_id: int):
    """Obtener planta del catálogo con estadísticas"""
    # Obtener la planta del catálogo
    plant = db.query(CatalogoPlanta).filter(
        CatalogoPlanta.id_catalogo == catalog_id
    ).first()
    
    if not plant:
        return None
    
    # Obtener estadísticas
    total_plantas = db.query(Planta).filter(
        Planta.id_catalogo == catalog_id,
        Planta.activa == True
    ).count()
    
    usuarios_activos = db.query(distinct(Planta.id_usuario)).filter(
        Planta.id_catalogo == catalog_id,
        Planta.activa == True
    ).count()
    
    stats = {
        'total_plantas': total_plantas,
        'usuarios_activos': usuarios_activos
    }
    
    return plant, stats

def get_catalog_plant_by_id(db: Session, catalog_id: int):
    """Obtener planta del catálogo por ID simple"""
    return db.query(CatalogoPlanta).filter(
        CatalogoPlanta.id_catalogo == catalog_id,
        CatalogoPlanta.activo == True
    ).first()