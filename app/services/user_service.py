from fastapi import HTTPException
from app.domain.repositories.user_repository import get_all_users, get_users_count
from app.domain.entities.user import UserResponse, DispositivoResponse, UsersListResponse

def get_all_users_service(db, skip: int = 0, limit: int = 100):
    """Obtener todos los usuarios con sus dispositivos"""
    try:
        # Validar parámetros
        if skip < 0:
            raise HTTPException(status_code=400, detail="Skip debe ser mayor o igual a 0")
        if limit <= 0 or limit > 100:
            raise HTTPException(status_code=400, detail="Limit debe estar entre 1 y 100")
        
        # Obtener usuarios
        users = get_all_users(db, skip, limit)
        total_users = get_users_count(db)
        
        # Convertir a response model
        users_response = []
        for user in users:
            dispositivos_response = [
                DispositivoResponse(
                    id_dispositivo=dispositivo.id_dispositivo,
                    mac_address=dispositivo.mac_address,
                    nombre_dispositivo=dispositivo.nombre_dispositivo,
                    fecha_asignacion=dispositivo.fecha_asignacion
                )
                for dispositivo in user.dispositivos
            ]
            
            user_response = UserResponse(
                id_usuario=user.id_usuario,
                nombre_completo=user.nombre_completo,
                telefono=user.telefono,
                correo=user.correo,
                usuario=user.usuario,
                fecha_registro=user.fecha_registro,
                dispositivos=dispositivos_response
            )
            users_response.append(user_response)
        
        return UsersListResponse(
            usuarios=users_response,
            total=total_users,
            skip=skip,
            limit=limit
        )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno al obtener usuarios: {str(e)}")

def get_user_by_id_service(db, user_id: int):
    """Obtener un usuario específico por ID"""
    try:
        from app.domain.repositories.user_repository import get_user_by_id
        
        user = get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # Convertir dispositivos a response model
        dispositivos_response = [
            DispositivoResponse(
                id_dispositivo=dispositivo.id_dispositivo,
                mac_address=dispositivo.mac_address,
                nombre_dispositivo=dispositivo.nombre_dispositivo,
                fecha_asignacion=dispositivo.fecha_asignacion
            )
            for dispositivo in user.dispositivos
        ]
        
        return UserResponse(
            id_usuario=user.id_usuario,
            nombre_completo=user.nombre_completo,
            telefono=user.telefono,
            correo=user.correo,
            usuario=user.usuario,
            fecha_registro=user.fecha_registro,
            dispositivos=dispositivos_response
        )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno al obtener usuario: {str(e)}")