from sqlalchemy.orm import Session
from app.infrastructure.database.models import Usuario

def create_user(db: Session, user_data):
    db_user = Usuario(**user_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    return db.query(Usuario).filter(Usuario.usuario == username).first()
