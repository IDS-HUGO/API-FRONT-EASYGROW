from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from app.core.security import hash_password, verify_password, create_jwt
from app.domain.repositories.user_repository import create_user, get_user_by_username
from app.infrastructure.email.send_credentials import send_credentials_email

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
    user = get_user_by_username(db, credentials.usuario)
    if user and verify_password(credentials.contrasena, user.contrasena):
        return create_jwt({"sub": user.usuario})
    return None
