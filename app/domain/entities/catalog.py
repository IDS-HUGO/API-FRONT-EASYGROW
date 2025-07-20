# app/domain/entities/catalog.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class CatalogPlantBasic(BaseModel):
    id_catalogo: int
    nombre_comun: str
    nombre_cientifico: str
    descripcion: Optional[str] = None
    altura_maxima_cm: Optional[int] = None
    imagen_referencia: Optional[str] = None
    activo: bool
    
    class Config:
        from_attributes = True

class CatalogPlantDetailResponse(CatalogPlantBasic):
    cuidados_especiales: Optional[str] = None
    fecha_creacion: datetime
    # Estadísticas adicionales
    total_plantas_registradas: int = 0
    usuarios_activos: int = 0

class CatalogListResponse(BaseModel):
    plantas: List[CatalogPlantBasic]
    total: int
    skip: int
    limit: int
    search_term: Optional[str] = None