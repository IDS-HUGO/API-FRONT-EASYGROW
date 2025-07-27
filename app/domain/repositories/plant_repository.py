from sqlalchemy.orm import Session, joinedload
from app.infrastructure.database.models import Planta, CatalogoPlanta, Usuario, Dispositivo

def create_plant(db: Session, plant_data: dict):
    """Crear una nueva planta"""
    db_plant = Planta(**plant_data)
    db.add(db_plant)
    db.commit()
    db.refresh(db_plant)
    return db_plant

def get_plant_with_catalog_info(db: Session, plant_id: int):
    """Obtener planta con información del catálogo"""
    return db.query(Planta).options(
        joinedload(Planta.catalogo_info)
    ).filter(Planta.id_planta == plant_id).first()

def check_catalog_exists(db: Session, catalog_id: int):
    """Verificar si existe una planta en el catálogo"""
    return db.query(CatalogoPlanta).filter(
        CatalogoPlanta.id_catalogo == catalog_id,
        CatalogoPlanta.activo == True
    ).first()

def check_user_exists(db: Session, user_id: int):
    """Verificar si existe el usuario"""
    return db.query(Usuario).filter(Usuario.id_usuario == user_id).first()

def check_device_exists_and_belongs_to_user(db: Session, device_id: int, user_id: int):
    """Verificar si el dispositivo existe y pertenece al usuario"""
    return db.query(Dispositivo).filter(
        Dispositivo.id_dispositivo == device_id,
        Dispositivo.id_usuario == user_id
    ).first()

def get_catalog_plant_by_id(db: Session, catalog_id: int):
    """Obtener información de planta del catálogo"""
    return db.query(CatalogoPlanta).filter(
        CatalogoPlanta.id_catalogo == catalog_id,
        CatalogoPlanta.activo == True
    ).first()

def get_plant_by_id_and_user(db: Session, plant_id: int, user_id: int):
    """Obtener planta por ID verificando que pertenezca al usuario"""
    return db.query(Planta).filter(
        Planta.id_planta == plant_id,
        Planta.id_usuario == user_id
    ).first()

def soft_delete_plant(db: Session, plant_id: int):
    """Realizar soft delete de una planta (marcar como inactiva)"""
    plant = db.query(Planta).filter(Planta.id_planta == plant_id).first()
    if plant:
        plant.activa = False
        db.commit()
        db.refresh(plant)
    return plant

def hard_delete_plant(db: Session, plant_id: int):
    """Eliminar permanentemente una planta de la base de datos"""
    plant = db.query(Planta).filter(Planta.id_planta == plant_id).first()
    if plant:
        db.delete(plant)
        db.commit()
        return True
    return False