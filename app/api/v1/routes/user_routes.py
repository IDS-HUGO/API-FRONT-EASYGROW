from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.domain.entities.user import UsersListResponse, UserResponse
from app.infrastructure.database.db import SessionLocal
from app.services.user_service import get_all_users_service, get_user_by_id_service

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=UsersListResponse)
def get_all_users(
    skip: int = Query(0, ge=0, description="Número de usuarios a omitir"),
    limit: int = Query(10, ge=1, le=100, description="Límite de usuarios por página"),
    db: Session = Depends(get_db)
):
    """
    Obtener todos los usuarios con paginación
    
    - **skip**: Número de usuarios a omitir (para paginación)
    - **limit**: Límite de usuarios por página (máximo 100)
    """
    try:
        result = get_all_users_service(db, skip, limit)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener un usuario específico por ID
    
    - **user_id**: ID del usuario a obtener
    """
    try:
        result = get_user_by_id_service(db, user_id)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.get("/search/username/{username}", response_model=UserResponse)
def get_user_by_username(
    username: str,
    db: Session = Depends(get_db)
):
    """
    Obtener un usuario por nombre de usuario
    
    - **username**: Nombre de usuario a buscar
    """
    try:
        from app.domain.repositories.user_repository import get_user_with_devices
        
        user = get_user_with_devices(db, username)
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # Convertir a response model
        from app.domain.entities.user import DispositivoResponse
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
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")