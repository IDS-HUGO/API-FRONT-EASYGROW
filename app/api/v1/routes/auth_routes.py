from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.domain.entities.user import UserCreate, UserLogin, LoginResponse
from app.infrastructure.database.db import SessionLocal
from app.services.auth_service import register_user, login_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        new_user = register_user(db, user)
        return {"msg": "Usuario registrado exitosamente", "usuario": new_user.usuario}
    except HTTPException as e:
        # Re-lanzar excepción para manejo de error en FastAPI
        raise e
    except Exception as e:
        # Error genérico
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.post("/login", response_model=LoginResponse)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    login_response = login_user(db, credentials)
    if not login_response:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    return login_response