from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc, and_, func
from datetime import datetime, timedelta
from typing import Optional
from app.infrastructure.database.models import (
    SensorDatos, LecturaDatos, Dispositivo
)
from app.domain.entities.sensor import (
    SensorListResponse, SensorDetailResponse, SensorResponse,
    ReadingListResponse, ReadingResponse, ReadingCreateRequest,
    ReadingCreateResponse, DeviceReadingsResponse, LatestReadingsResponse,
    SENSOR_TYPES, SENSOR_UNITS
)

def get_device_sensors_service(db: Session, device_id: int):
    """Obtener todos los sensores de un dispositivo específico"""
    try:
        # Verificar que el dispositivo existe
        device = db.query(Dispositivo).filter(Dispositivo.id_dispositivo == device_id).first()
        if not device:
            raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
        
        sensores = db.query(SensorDatos).filter(
            SensorDatos.id_dispositivo == device_id
        ).order_by(SensorDatos.tipo_sensor).all()
        
        sensor_responses = []
        for sensor in sensores:
            sensor_responses.append(SensorResponse(
                id_sensor=sensor.id_sensor,
                tipo_sensor=sensor.tipo_sensor,
                unidad_medida=sensor.unidad_medida,
                descripcion=sensor.descripcion,
                id_dispositivo=sensor.id_dispositivo
            ))
        
        return SensorListResponse(
            sensores=sensor_responses,
            dispositivo_id=device_id,
            total_sensores=len(sensor_responses)
        )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener sensores: {str(e)}")

def get_sensor_detail_service(db: Session, sensor_id: int):
    """Obtener detalles de un sensor específico"""
    try:
        sensor = db.query(SensorDatos).filter(SensorDatos.id_sensor == sensor_id).first()
        if not sensor:
            raise HTTPException(status_code=404, detail="Sensor no encontrado")
        
        # Obtener estadísticas del sensor
        total_lecturas = db.query(LecturaDatos).filter(
            LecturaDatos.id_sensor == sensor_id
        ).count()
        
        ultima_lectura_query = db.query(LecturaDatos).filter(
            LecturaDatos.id_sensor == sensor_id
        ).order_by(desc(LecturaDatos.fecha_hora)).first()
        
        ultima_lectura = None
        if ultima_lectura_query:
            ultima_lectura = ultima_lectura_query.fecha_hora
        
        # Promedio últimas 24 horas
        hace_24h = datetime.utcnow() - timedelta(hours=24)
        promedio_24h = db.query(func.avg(LecturaDatos.valor)).filter(
            and_(
                LecturaDatos.id_sensor == sensor_id,
                LecturaDatos.fecha_hora >= hace_24h
            )
        ).scalar()
        
        # Información del dispositivo
        device = db.query(Dispositivo).filter(
            Dispositivo.id_dispositivo == sensor.id_dispositivo
        ).first()
        
        dispositivo_info = None
        if device:
            dispositivo_info = {
                "id_dispositivo": device.id_dispositivo,
                "mac_address": device.mac_address,
                "nombre_dispositivo": device.nombre_dispositivo
            }
        
        return SensorDetailResponse(
            id_sensor=sensor.id_sensor,
            tipo_sensor=sensor.tipo_sensor,
            unidad_medida=sensor.unidad_medida,
            descripcion=sensor.descripcion,
            id_dispositivo=sensor.id_dispositivo,
            dispositivo_info=dispositivo_info,
            total_lecturas=total_lecturas,
            ultima_lectura=ultima_lectura,
            promedio_24h=float(promedio_24h) if promedio_24h else None
        )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener sensor: {str(e)}")

def get_sensor_readings_service(
    db: Session, 
    sensor_id: int, 
    skip: int = 0, 
    limit: int = 100, 
    date_from: Optional[datetime] = None, 
    date_to: Optional[datetime] = None
):
    """Obtener lecturas de un sensor específico con filtros de fecha"""
    try:
        # Verificar que el sensor existe
        sensor = db.query(SensorDatos).filter(SensorDatos.id_sensor == sensor_id).first()
        if not sensor:
            raise HTTPException(status_code=404, detail="Sensor no encontrado")
        
        query = db.query(LecturaDatos).filter(LecturaDatos.id_sensor == sensor_id)
        
        # Aplicar filtros de fecha
        if date_from:
            query = query.filter(LecturaDatos.fecha_hora >= date_from)
        if date_to:
            query = query.filter(LecturaDatos.fecha_hora <= date_to)
        
        # Contar total
        total = query.count()
        
        # Aplicar paginación y ordenar
        lecturas = query.order_by(desc(LecturaDatos.fecha_hora)).offset(skip).limit(limit).all()
        
        # Convertir a formato de respuesta
        reading_responses = []
        for lectura in lecturas:
            reading_responses.append(ReadingResponse(
                id_lectura=lectura.id_lectura,
                valor=lectura.valor,
                fecha_hora=lectura.fecha_hora,
                id_sensor=lectura.id_sensor,
                tipo_sensor=sensor.tipo_sensor,
                unidad_medida=sensor.unidad_medida
            ))
        
        date_range = None
        if date_from or date_to:
            date_range = {
                "date_from": date_from.isoformat() if date_from else None,
                "date_to": date_to.isoformat() if date_to else None
            }
        
        return ReadingListResponse(
            lecturas=reading_responses,
            sensor_id=sensor_id,
            total=total,
            skip=skip,
            limit=limit,
            date_range=date_range
        )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener lecturas: {str(e)}")

def get_device_readings_service(
    db: Session, 
    device_id: int, 
    skip: int = 0, 
    limit: int = 100,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    sensor_type: Optional[str] = None
):
    """Obtener todas las lecturas de todos los sensores de un dispositivo"""
    try:
        # Verificar que el dispositivo existe
        device = db.query(Dispositivo).filter(Dispositivo.id_dispositivo == device_id).first()
        if not device:
            raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
        
        # Subconsulta para obtener sensores del dispositivo
        sensor_subquery = db.query(SensorDatos.id_sensor).filter(
            SensorDatos.id_dispositivo == device_id
        )
        
        if sensor_type:
            sensor_subquery = sensor_subquery.filter(SensorDatos.tipo_sensor == sensor_type)
        
        sensor_ids = [s[0] for s in sensor_subquery.all()]
        
        if not sensor_ids:
            return DeviceReadingsResponse(
                lecturas=[],
                dispositivo_id=device_id,
                total=0,
                skip=skip,
                limit=limit,
                sensores_incluidos=[],
                date_range=None
            )
        
        # Query principal para lecturas
        query = db.query(LecturaDatos).join(SensorDatos).filter(
            LecturaDatos.id_sensor.in_(sensor_ids)
        )
        
        # Aplicar filtros de fecha
        if date_from:
            query = query.filter(LecturaDatos.fecha_hora >= date_from)
        if date_to:
            query = query.filter(LecturaDatos.fecha_hora <= date_to)
        
        # Contar total
        total = query.count()
        
        # Obtener lecturas con información del sensor
        lecturas = query.order_by(desc(LecturaDatos.fecha_hora)).offset(skip).limit(limit).all()
        
        # Convertir a formato de respuesta
        reading_responses = []
        sensores_incluidos = set()
        
        for lectura in lecturas:
            sensor = db.query(SensorDatos).filter(
                SensorDatos.id_sensor == lectura.id_sensor
            ).first()
            
            if sensor:
                reading_responses.append(ReadingResponse(
                    id_lectura=lectura.id_lectura,
                    valor=lectura.valor,
                    fecha_hora=lectura.fecha_hora,
                    id_sensor=lectura.id_sensor,
                    tipo_sensor=sensor.tipo_sensor,
                    unidad_medida=sensor.unidad_medida
                ))
                sensores_incluidos.add(sensor.tipo_sensor)
        
        date_range = None
        if date_from or date_to:
            date_range = {
                "date_from": date_from.isoformat() if date_from else None,
                "date_to": date_to.isoformat() if date_to else None
            }
        
        return DeviceReadingsResponse(
            lecturas=reading_responses,
            dispositivo_id=device_id,
            total=total,
            skip=skip,
            limit=limit,
            sensores_incluidos=list(sensores_incluidos),
            date_range=date_range
        )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener lecturas del dispositivo: {str(e)}")

def get_latest_readings_service(db: Session, device_id: int):
    """Obtener las últimas lecturas de cada sensor del dispositivo"""
    try:
        # Verificar que el dispositivo existe
        device = db.query(Dispositivo).filter(Dispositivo.id_dispositivo == device_id).first()
        if not device:
            raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
        
        # Obtener sensores del dispositivo
        sensores = db.query(SensorDatos).filter(
            SensorDatos.id_dispositivo == device_id
        ).all()
        
        lecturas_por_sensor = []
        ultima_actualizacion = None
        
        for sensor in sensores:
            # Obtener la última lectura de cada sensor
            ultima_lectura = db.query(LecturaDatos).filter(
                LecturaDatos.id_sensor == sensor.id_sensor
            ).order_by(desc(LecturaDatos.fecha_hora)).first()
            
            if ultima_lectura:
                if not ultima_actualizacion or ultima_lectura.fecha_hora > ultima_actualizacion:
                    ultima_actualizacion = ultima_lectura.fecha_hora
                
                lecturas_por_sensor.append({
                    "sensor_info": {
                        "id_sensor": sensor.id_sensor,
                        "tipo_sensor": sensor.tipo_sensor,
                        "unidad_medida": sensor.unidad_medida,
                        "descripcion": sensor.descripcion
                    },
                    "ultima_lectura": {
                        "id_lectura": ultima_lectura.id_lectura,
                        "valor": ultima_lectura.valor,
                        "fecha_hora": ultima_lectura.fecha_hora
                    }
                })
        
        if not ultima_actualizacion:
            ultima_actualizacion = datetime.utcnow()
        
        return LatestReadingsResponse(
            dispositivo_id=device_id,
            ultima_actualizacion=ultima_actualizacion,
            lecturas_por_sensor=lecturas_por_sensor
        )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener últimas lecturas: {str(e)}")

def create_reading_service(db: Session, reading: ReadingCreateRequest):
    """Crear una nueva lectura de sensor"""
    try:
        # Verificar que el sensor existe
        sensor = db.query(SensorDatos).filter(
            SensorDatos.id_sensor == reading.id_sensor
        ).first()
        
        if not sensor:
            raise HTTPException(status_code=404, detail="Sensor no encontrado")
        
        # Crear la lectura
        nueva_lectura = LecturaDatos(
            valor=reading.valor,
            id_sensor=reading.id_sensor,
            fecha_hora=datetime.utcnow()
        )
        
        db.add(nueva_lectura)
        db.commit()
        db.refresh(nueva_lectura)
        
        # Crear respuesta
        reading_response = ReadingResponse(
            id_lectura=nueva_lectura.id_lectura,
            valor=nueva_lectura.valor,
            fecha_hora=nueva_lectura.fecha_hora,
            id_sensor=nueva_lectura.id_sensor,
            tipo_sensor=sensor.tipo_sensor,
            unidad_medida=sensor.unidad_medida
        )
        
        return ReadingCreateResponse(
            msg="Lectura creada exitosamente",
            lectura=reading_response
        )
        
    except HTTPException as e:
        db.rollback()
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear lectura: {str(e)}")

def get_device_sensor_readings_by_type_service(
    db: Session, 
    device_id: int, 
    sensor_type: str, 
    skip: int = 0, 
    limit: int = 50, 
    hours: int = 24
):
    """Obtener lecturas de un tipo específico de sensor en las últimas X horas"""
    try:
        # Verificar que el dispositivo existe
        device = db.query(Dispositivo).filter(Dispositivo.id_dispositivo == device_id).first()
        if not device:
            raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
        
        # Calcular fecha límite
        fecha_limite = datetime.utcnow() - timedelta(hours=hours)
        
        # Obtener sensores del tipo especificado
        sensores = db.query(SensorDatos).filter(
            and_(
                SensorDatos.id_dispositivo == device_id,
                SensorDatos.tipo_sensor == sensor_type
            )
        ).all()
        
        if not sensores:
            return {
                "dispositivo_id": device_id,
                "sensor_type": sensor_type,
                "lecturas": [],
                "total": 0,
                "periodo": f"últimas {hours} horas"
            }
        
        sensor_ids = [s.id_sensor for s in sensores]
        
        # Query para obtener lecturas
        query = db.query(LecturaDatos).filter(
            and_(
                LecturaDatos.id_sensor.in_(sensor_ids),
                LecturaDatos.fecha_hora >= fecha_limite
            )
        )
        
        total = query.count()
        
        lecturas = query.order_by(desc(LecturaDatos.fecha_hora)).offset(skip).limit(limit).all()
        
        # Convertir a formato de respuesta
        reading_responses = []
        for lectura in lecturas:
            sensor = next((s for s in sensores if s.id_sensor == lectura.id_sensor), None)
            if sensor:
                reading_responses.append(ReadingResponse(
                    id_lectura=lectura.id_lectura,
                    valor=lectura.valor,
                    fecha_hora=lectura.fecha_hora,
                    id_sensor=lectura.id_sensor,
                    tipo_sensor=sensor.tipo_sensor,
                    unidad_medida=sensor.unidad_medida
                ))
        
        return {
            "dispositivo_id": device_id,
            "sensor_type": sensor_type,
            "lecturas": reading_responses,
            "total": total,
            "skip": skip,
            "limit": limit,
            "periodo": f"últimas {hours} horas",
            "sensores_incluidos": len(sensores)
        }
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener lecturas por tipo: {str(e)}")
