from sqlalchemy.orm import Session
from app.infrastructure.database.models import Dispositivo, Usuario

def create_device(db: Session, device_data: dict):
    """Crear un nuevo dispositivo"""
    db_device = Dispositivo(**device_data)
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device

def get_device_by_mac(db: Session, mac_address: str):
    """Obtener dispositivo por MAC address"""
    return db.query(Dispositivo).filter(Dispositivo.mac_address == mac_address).first()

def get_user_devices(db: Session, user_id: int):
    """Obtener todos los dispositivos de un usuario"""
    return db.query(Dispositivo).filter(Dispositivo.id_usuario == user_id).all()

def check_device_exists(db: Session, mac_address: str):
    """Verificar si un dispositivo ya existe"""
    return db.query(Dispositivo).filter(Dispositivo.mac_address == mac_address).first() is not None

def get_user_by_id(db: Session, user_id: int):
    """Obtener usuario por ID"""
    return db.query(Usuario).filter(Usuario.id_usuario == user_id).first()

def get_device_by_id(db: Session, device_id: int):
    """Obtener dispositivo por ID"""
    return db.query(Dispositivo).filter(Dispositivo.id_dispositivo == device_id).first()

def update_device_name(db: Session, device_id: int, nombre_dispositivo: str):
    """Actualizar nombre del dispositivo"""
    device = db.query(Dispositivo).filter(Dispositivo.id_dispositivo == device_id).first()
    if device:
        device.nombre_dispositivo = nombre_dispositivo
        db.commit()
        db.refresh(device)
    return device