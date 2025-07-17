from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from app.domain.repositories.device_repository import (
    create_device, 
    check_device_exists, 
    get_user_by_id
)
from app.domain.entities.device import DeviceResponse, DeviceAssignResponse

def assign_device_to_user(db, device_request):
    """Asignar un dispositivo a un usuario usando datos del body"""
    try:
        # Verificar que el usuario existe
        user = get_user_by_id(db, device_request.user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # Verificar si el dispositivo ya existe
        if check_device_exists(db, device_request.mac_address):
            raise HTTPException(
                status_code=400, 
                detail="El dispositivo con esta MAC address ya está registrado"
            )
        
        # Crear los datos del dispositivo
        device_dict = {
            "mac_address": device_request.mac_address,
            "nombre_dispositivo": device_request.nombre_dispositivo,
            "id_usuario": device_request.user_id
        }
        
        # Crear el dispositivo
        new_device = create_device(db, device_dict)
        
        # Crear respuesta
        device_response = DeviceResponse(
            id_dispositivo=new_device.id_dispositivo,
            mac_address=new_device.mac_address,
            nombre_dispositivo=new_device.nombre_dispositivo,
            fecha_asignacion=new_device.fecha_asignacion,
            id_usuario=new_device.id_usuario
        )
        
        return DeviceAssignResponse(
            msg="Dispositivo asignado exitosamente",
            dispositivo=device_response
        )
        
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, 
            detail="Error de integridad: El dispositivo ya está registrado"
        )
    except HTTPException as e:
        db.rollback()
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, 
            detail=f"Error interno al asignar dispositivo: {str(e)}"
        )