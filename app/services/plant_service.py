from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_
from app.infrastructure.database.models import Planta, CatalogoPlanta, Dispositivo
from app.domain.entities.plant import (
    UserPlantsResponse, DevicePlantsResponse, UserDevicePlantsResponse, 
    PlantDetailResponse, PlantResponse, CatalogPlantInfo
)
from fastapi import HTTPException

def get_user_plants_service(db: Session, user_id: int, active_only: bool = True):
    """Obtener todas las plantas de un usuario específico"""
    try:
        query = db.query(Planta).options(
            joinedload(Planta.catalogo_info),
            joinedload(Planta.dispositivo)
        ).filter(Planta.id_usuario == user_id)
        
        if active_only:
            query = query.filter(Planta.activa == True)
        
        plantas_db = query.order_by(Planta.fecha_registro.desc()).all()
        
        # Convertir a formato de respuesta
        plantas = []
        for planta in plantas_db:
            catalog_info = CatalogPlantInfo(
                id_catalogo=planta.catalogo_info.id_catalogo,
                nombre_comun=planta.catalogo_info.nombre_comun,
                nombre_cientifico=planta.catalogo_info.nombre_cientifico,
                descripcion=planta.catalogo_info.descripcion,
                altura_maxima_cm=planta.catalogo_info.altura_maxima_cm,
                cuidados_especiales=planta.catalogo_info.cuidados_especiales
            )
            
            plant_response = PlantResponse(
                id_planta=planta.id_planta,
                id_catalogo=planta.id_catalogo,
                id_usuario=planta.id_usuario,
                id_dispositivo=planta.id_dispositivo,
                nombre_personalizado=planta.nombre_personalizado,
                ubicacion=planta.ubicacion,
                fecha_plantacion=planta.fecha_plantacion,
                fecha_registro=planta.fecha_registro,
                notas_usuario=planta.notas_usuario,
                activa=planta.activa,
                catalogo_info=catalog_info
            )
            plantas.append(plant_response)
        
        # Estadísticas
        total_plantas = len(plantas)
        plantas_activas = len([p for p in plantas if p.activa])
        plantas_con_dispositivo = len([p for p in plantas if p.id_dispositivo])
        
        return UserPlantsResponse(
            user_id=user_id,
            plantas=plantas,
            total_plantas=total_plantas,
            plantas_activas=plantas_activas,
            plantas_con_dispositivo=plantas_con_dispositivo
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener plantas del usuario: {str(e)}")

def get_device_plants_service(db: Session, device_id: int, active_only: bool = True):
    """Obtener plantas monitoreadas por un dispositivo específico"""
    try:
        # Obtener información del dispositivo
        device = db.query(Dispositivo).filter(Dispositivo.id_dispositivo == device_id).first()
        if not device:
            raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
        
        query = db.query(Planta).options(
            joinedload(Planta.catalogo_info)
        ).filter(Planta.id_dispositivo == device_id)
        
        if active_only:
            query = query.filter(Planta.activa == True)
        
        plantas_db = query.order_by(Planta.fecha_registro.desc()).all()
        
        # Convertir a formato de respuesta
        plantas = []
        for planta in plantas_db:
            catalog_info = CatalogPlantInfo(
                id_catalogo=planta.catalogo_info.id_catalogo,
                nombre_comun=planta.catalogo_info.nombre_comun,
                nombre_cientifico=planta.catalogo_info.nombre_cientifico,
                descripcion=planta.catalogo_info.descripcion,
                altura_maxima_cm=planta.catalogo_info.altura_maxima_cm,
                cuidados_especiales=planta.catalogo_info.cuidados_especiales
            )
            
            plant_response = PlantResponse(
                id_planta=planta.id_planta,
                id_catalogo=planta.id_catalogo,
                id_usuario=planta.id_usuario,
                id_dispositivo=planta.id_dispositivo,
                nombre_personalizado=planta.nombre_personalizado,
                ubicacion=planta.ubicacion,
                fecha_plantacion=planta.fecha_plantacion,
                fecha_registro=planta.fecha_registro,
                notas_usuario=planta.notas_usuario,
                activa=planta.activa,
                catalogo_info=catalog_info
            )
            plantas.append(plant_response)
        
        return DevicePlantsResponse(
            device_id=device_id,
            mac_address=device.mac_address,
            nombre_dispositivo=device.nombre_dispositivo,
            plantas=plantas,
            total_plantas=len(plantas)
        )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener plantas del dispositivo: {str(e)}")

def get_user_device_plants_service(db: Session, user_id: int, device_id: int, active_only: bool = True):
    """Obtener plantas de un usuario específico monitoreadas por un dispositivo específico"""
    try:
        query = db.query(Planta).options(
            joinedload(Planta.catalogo_info)
        ).filter(
            and_(
                Planta.id_usuario == user_id,
                Planta.id_dispositivo == device_id
            )
        )
        
        if active_only:
            query = query.filter(Planta.activa == True)
        
        plantas_db = query.order_by(Planta.fecha_registro.desc()).all()
        
        # Convertir a formato de respuesta
        plantas = []
        for planta in plantas_db:
            catalog_info = CatalogPlantInfo(
                id_catalogo=planta.catalogo_info.id_catalogo,
                nombre_comun=planta.catalogo_info.nombre_comun,
                nombre_cientifico=planta.catalogo_info.nombre_cientifico,
                descripcion=planta.catalogo_info.descripcion,
                altura_maxima_cm=planta.catalogo_info.altura_maxima_cm,
                cuidados_especiales=planta.catalogo_info.cuidados_especiales
            )
            
            plant_response = PlantResponse(
                id_planta=planta.id_planta,
                id_catalogo=planta.id_catalogo,
                id_usuario=planta.id_usuario,
                id_dispositivo=planta.id_dispositivo,
                nombre_personalizado=planta.nombre_personalizado,
                ubicacion=planta.ubicacion,
                fecha_plantacion=planta.fecha_plantacion,
                fecha_registro=planta.fecha_registro,
                notas_usuario=planta.notas_usuario,
                activa=planta.activa,
                catalogo_info=catalog_info
            )
            plantas.append(plant_response)
        
        return UserDevicePlantsResponse(
            user_id=user_id,
            device_id=device_id,
            plantas=plantas,
            total_plantas=len(plantas)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener plantas del usuario y dispositivo: {str(e)}")

def get_plant_detail_service(db: Session, plant_id: int):
    """Obtener detalles completos de una planta específica"""
    try:
        planta = db.query(Planta).options(
            joinedload(Planta.catalogo_info),
            joinedload(Planta.dispositivo)
        ).filter(Planta.id_planta == plant_id).first()
        
        if not planta:
            raise HTTPException(status_code=404, detail="Planta no encontrada")
        
        # Información del catálogo
        catalog_info = CatalogPlantInfo(
            id_catalogo=planta.catalogo_info.id_catalogo,
            nombre_comun=planta.catalogo_info.nombre_comun,
            nombre_cientifico=planta.catalogo_info.nombre_cientifico,
            descripcion=planta.catalogo_info.descripcion,
            altura_maxima_cm=planta.catalogo_info.altura_maxima_cm,
            cuidados_especiales=planta.catalogo_info.cuidados_especiales
        )
        
        # Calcular días desde plantación
        dias_desde_plantacion = None
        if planta.fecha_plantacion:
            from datetime import date
            dias_desde_plantacion = (date.today() - planta.fecha_plantacion).days
        
        # Información del dispositivo
        dispositivo_info = None
        if planta.dispositivo:
            dispositivo_info = {
                "id_dispositivo": planta.dispositivo.id_dispositivo,
                "mac_address": planta.dispositivo.mac_address,
                "nombre_dispositivo": planta.dispositivo.nombre_dispositivo,
                "fecha_asignacion": planta.dispositivo.fecha_asignacion
            }
        
        return PlantDetailResponse(
            id_planta=planta.id_planta,
            id_catalogo=planta.id_catalogo,
            id_usuario=planta.id_usuario,
            id_dispositivo=planta.id_dispositivo,
            nombre_personalizado=planta.nombre_personalizado,
            ubicacion=planta.ubicacion,
            fecha_plantacion=planta.fecha_plantacion,
            fecha_registro=planta.fecha_registro,
            notas_usuario=planta.notas_usuario,
            activa=planta.activa,
            catalogo_info=catalog_info,
            dias_desde_plantacion=dias_desde_plantacion,
            dispositivo_info=dispositivo_info,
            ultimas_lecturas=None,  # Se puede implementar después
            estadisticas_sensores=None  # Se puede implementar después
        )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener detalle de la planta: {str(e)}")
def create_plant_service(db, plant_request):
    """
    Crear una nueva planta asociada a un usuario y dispositivo.
    """
    from app.domain.repositories.plant_repository import create_plant, check_catalog_exists, check_user_exists, check_device_exists_and_belongs_to_user
    from app.domain.entities.plant import PlantCreateResponse, PlantResponse, CatalogPlantInfo

    # Validar existencia de catálogo
    catalog = check_catalog_exists(db, plant_request.id_catalogo)
    if not catalog:
        raise HTTPException(status_code=404, detail="Planta del catálogo no encontrada")

    # Validar existencia de usuario
    user = check_user_exists(db, plant_request.id_usuario)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Validar dispositivo si se proporciona
    if plant_request.id_dispositivo:
        device = check_device_exists_and_belongs_to_user(db, plant_request.id_dispositivo, plant_request.id_usuario)
        if not device:
            raise HTTPException(status_code=404, detail="El dispositivo no existe o no pertenece al usuario")

    # Crear la planta
    plant_data = plant_request.dict()
    new_plant = create_plant(db, plant_data)

    # Construir respuesta
    catalog_info = CatalogPlantInfo(
        id_catalogo=catalog.id_catalogo,
        nombre_comun=catalog.nombre_comun,
        nombre_cientifico=catalog.nombre_cientifico,
        descripcion=catalog.descripcion,
        altura_maxima_cm=catalog.altura_maxima_cm,
        cuidados_especiales=catalog.cuidados_especiales
    )

    plant_response = PlantResponse(
        id_planta=new_plant.id_planta,
        id_catalogo=new_plant.id_catalogo,
        id_usuario=new_plant.id_usuario,
        id_dispositivo=new_plant.id_dispositivo,
        nombre_personalizado=new_plant.nombre_personalizado,
        ubicacion=new_plant.ubicacion,
        fecha_plantacion=new_plant.fecha_plantacion,
        fecha_registro=new_plant.fecha_registro,
        notas_usuario=new_plant.notas_usuario,
        activa=new_plant.activa,
        catalogo_info=catalog_info
    )

    return PlantCreateResponse(
        msg="Planta creada exitosamente",
        planta=plant_response
    )
def delete_plant_service(db: Session, plant_id: int, user_id: int):
    """Eliminar una planta (soft delete)"""
    from app.domain.repositories.plant_repository import get_plant_by_id_and_user, soft_delete_plant
    from app.domain.entities.plant import PlantDeleteResponse
    
    try:
        # Verificar que la planta existe y pertenece al usuario
        plant = get_plant_by_id_and_user(db, plant_id, user_id)
        if not plant:
            raise HTTPException(
                status_code=404, 
                detail="Planta no encontrada o no tienes permisos para eliminarla"
            )
        
        # Verificar si ya está inactiva
        if not plant.activa:
            raise HTTPException(
                status_code=400, 
                detail="La planta ya está eliminada"
            )
        
        # Realizar soft delete
        deleted_plant = soft_delete_plant(db, plant_id)
        
        return PlantDeleteResponse(
            msg="Planta eliminada exitosamente",
            plant_id=plant_id,
            deleted_permanently=False
        )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar la planta: {str(e)}")

def delete_plant_permanent_service(db: Session, plant_id: int, user_id: int):
    """Eliminar permanentemente una planta"""
    from app.domain.repositories.plant_repository import get_plant_by_id_and_user, hard_delete_plant
    from app.domain.entities.plant import PlantDeleteResponse
    
    try:
        # Verificar que la planta existe y pertenece al usuario
        plant = get_plant_by_id_and_user(db, plant_id, user_id)
        if not plant:
            raise HTTPException(
                status_code=404, 
                detail="Planta no encontrada o no tienes permisos para eliminarla"
            )
        
        # Eliminar permanentemente
        deleted = hard_delete_plant(db, plant_id)
        
        if deleted:
            return PlantDeleteResponse(
                msg="Planta eliminada permanentemente",
                plant_id=plant_id,
                deleted_permanently=True
            )
        else:
            raise HTTPException(status_code=500, detail="Error al eliminar la planta")
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar permanentemente la planta: {str(e)}")
