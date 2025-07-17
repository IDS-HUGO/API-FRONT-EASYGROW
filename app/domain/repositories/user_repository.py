from sqlalchemy.orm import Session
from app.infrastructure.database.models import Usuario, Dispositivo

def create_user(db: Session, user_data):
    db_user = Usuario(**user_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    return db.query(Usuario).filter(Usuario.usuario == username).first()

def get_user_with_devices(db: Session, username: str):
    """Obtiene usuario con sus dispositivos asociados"""
    return db.query(Usuario).filter(Usuario.usuario == username).first()

def get_user_devices(db: Session, user_id: int):
    """Obtiene todos los dispositivos asociados a un usuario"""
    return db.query(Dispositivo).filter(Dispositivo.id_usuario == user_id).all()

def get_all_users(db: Session, skip: int = 0, limit: int = 100):
    """Obtiene todos los usuarios con paginación"""
    return db.query(Usuario).offset(skip).limit(limit).all()

def get_users_count(db: Session):
    """Obtiene el total de usuarios registrados"""
    return db.query(Usuario).count()

def get_user_by_id(db: Session, user_id: int):
    """Obtiene usuario por ID"""
    return db.query(Usuario).filter(Usuario.id_usuario == user_id).first()