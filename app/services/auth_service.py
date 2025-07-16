from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from app.core.security import hash_password, verify_password, create_jwt
from app.domain.repositories.user_repository import create_user, get_user_with_devices
from app.infrastructure.email.send_credentials import send_credentials_email
from app.domain.entities.user import UserResponse, DispositivoResponse, LoginResponse

def register_user(db, user):
    try:
        hashed = hash_password(user.contrasena)
        user_data = user.dict()
        user_data["contrasena"] = hashed
        new_user = create_user(db, user_data)

        email_body = f"""
Hola {user.nombre_completo},

🪴Bienvenido a EasyGrow.🪴 Aquí están tus credenciales para acceder a la plataforma:

Usuario: {user.usuario}
Contraseña: {user.contrasena}

Si tienes dudas o necesitas ayuda, contáctanos.

Saludos cordiales,
Equipo EasyGrow ☘️🌻
        """

        send_credentials_email(
            to=user.correo,
            subject="Tus credenciales de acceso a EasyGrow",
            body=email_body
        )
        return new_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="El nombre de usuario ya existe. Por favor elige otro.")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error interno al registrar usuario: {str(e)}")

def login_user(db, credentials):
    user = get_user_with_devices(db, credentials.usuario)
    if user and verify_password(credentials.contrasena, user.contrasena):
        # Crear token JWT
        token = create_jwt({"sub": user.usuario})
        
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
        
        # Crear respuesta del usuario
        user_response = UserResponse(
            id_usuario=user.id_usuario,
            nombre_completo=user.nombre_completo,
            telefono=user.telefono,
            correo=user.correo,
            usuario=user.usuario,
            fecha_registro=user.fecha_registro,
            dispositivos=dispositivos_response
        )
        
        # Retornar respuesta completa
        return LoginResponse(
            access_token=token,
            token_type="bearer",
            user_info=user_response
        )
    return None