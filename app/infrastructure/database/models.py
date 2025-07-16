from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
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
    
    # Relación con dispositivos
    dispositivos = relationship("Dispositivo", back_populates="usuario")

class Dispositivo(Base):
    __tablename__ = "dispositivo"

    id_dispositivo = Column(Integer, primary_key=True, index=True)
    mac_address = Column(String(17), nullable=False, unique=True)
    nombre_dispositivo = Column(String(100))
    fecha_asignacion = Column(DateTime, default=datetime.utcnow)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"))
    
    # Relación con usuario
    usuario = relationship("Usuario", back_populates="dispositivos")

class Imagen(Base):
    __tablename__ = "imagen"

    id_imagen = Column(Integer, primary_key=True, index=True)
    ruta_archivo = Column(String(255), nullable=False)
    fecha_hora = Column(DateTime, default=datetime.utcnow)
    id_dispositivo = Column(Integer, ForeignKey("dispositivo.id_dispositivo"))

class Planta(Base):
    __tablename__ = "planta"

    id_planta = Column(Integer, primary_key=True, index=True)
    nombre_comun = Column(String(100), nullable=False)
    nombre_cientifico = Column(String(150), nullable=False)
    descripcion = Column(Text)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    id_imagen = Column(Integer, ForeignKey("imagen.id_imagen"))
    fecha_registro = Column(DateTime, default=datetime.utcnow)

class SensorDatos(Base):
    __tablename__ = "sensor_datos"

    id_sensor = Column(Integer, primary_key=True, index=True)
    tipo_sensor = Column(String(50), nullable=False)
    unidad_medida = Column(String(20), nullable=False)
    descripcion = Column(Text)
    id_dispositivo = Column(Integer, ForeignKey("dispositivo.id_dispositivo"))

class LecturaDatos(Base):
    __tablename__ = "lectura_datos"

    id_lectura = Column(Integer, primary_key=True, index=True)
    valor = Column(Float, nullable=False)
    fecha_hora = Column(DateTime, default=datetime.utcnow)
    id_sensor = Column(Integer, ForeignKey("sensor_datos.id_sensor"))