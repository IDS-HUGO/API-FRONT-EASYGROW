from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre_completo = Column(String(100), nullable=False)
    telefono = Column(String(15))
    correo = Column(String(100), unique=True, nullable=False)
    usuario = Column(String(50), unique=True)
    contrasena = Column(String(255))
    fecha_registro = Column(DateTime, default=datetime.utcnow)
