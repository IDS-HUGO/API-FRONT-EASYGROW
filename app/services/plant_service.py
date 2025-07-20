from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from app.domain.repositories.plant_repository import (
    create_plant,
    check_catalog_exists,
    check_user_exists, 
    check_device_exists_and_belongs_to_user,
    get_catalog_plant_by_id
)
from app.domain.entities.plant import PlantResponse, PlantCreateResponse, CatalogPlantInfo

def create_plant_service(db, plant_request):
    """Crear una nueva planta con todas las validaciones"""
    try:
        # 1. Verificar que el catálogo de planta existe y está activo
        catalog_plant = check_catalog_exists(db, plant_request.id_catalogo)
        if not catalog_plant:
            raise HTTPException(
                status_code=404, 
                detail="La planta especificada no existe en el catálogo o está inactiva"
            )
        
        # 2. Verificar que el usuario existe
        user = check_user_exists(db, plant_request.id_usuario)
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # 3. Si se especifica dispositivo, verificar que existe y pertenece al usuario
        if plant_request.id_dispositivo:
            device = check_device_exists_and_belongs_to_user(
                db, plant_request.id_dispositivo, plant_request.id_usuario
            )
            if not device:
                raise HTTPException(
                    status_code=400, 
                    detail="El dispositivo no existe o no pertenece al usuario especificado"
                )
        
        # 4. Crear los datos de la planta
        plant_dict = {
            "id_catalogo": plant_request.id_catalogo,
            "id_usuario": plant_request.id_usuario,
            "id_dispositivo": plant_request.id_dispositivo,
            "nombre_personalizado": plant_request.nombre_personalizado,
            "ubicacion": plant_request.ubicacion,
            "fecha_plantacion": plant_request.fecha_plantacion,
            "notas_usuario": plant_request.notas_usuario,
            "activa": True
        }
        
        # 5. Crear la planta
        new_plant = create_plant(db, plant_dict)
        
        # 6. Obtener información completa del catálogo para la respuesta
        catalog_info = get_catalog_plant_by_id(db, plant_request.id_catalogo)
        
        # 7. Crear respuesta completa
        catalog_response = CatalogPlantInfo(
            id_catalogo=catalog_info.id_catalogo,
            nombre_comun=catalog_info.nombre_comun,
            nombre_cientifico=catalog_info.nombre_cientifico,
            descripcion=catalog_info.descripcion,
            altura_maxima_cm=catalog_info.altura_maxima_cm,
            cuidados_especiales=catalog_info.cuidados_especiales
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
            catalogo_info=catalog_response
        )
        
        return PlantCreateResponse(
            msg=f"Planta '{catalog_info.nombre_comun}' creada exitosamente",
            planta=plant_response
        )
        
    except IntegrityError as e:
        db.rollback()
        # Analizar el error de integridad para dar mensaje más específico
        if "id_catalogo" in str(e):
            raise HTTPException(status_code=400, detail="Error: Planta del catálogo no válida")
        elif "id_usuario" in str(e):
            raise HTTPException(status_code=400, detail="Error: Usuario no válido")
        elif "id_dispositivo" in str(e):
            raise HTTPException(status_code=400, detail="Error: Dispositivo no válido")
        else:
            raise HTTPException(status_code=400, detail="Error de integridad en la base de datos")
            
    except HTTPException as e:
        db.rollback()
        raise e
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, 
            detail=f"Error interno al crear la planta: {str(e)}"
        )