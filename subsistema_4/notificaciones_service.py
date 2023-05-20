from datetime import datetime
from schemas.database import SessionLocal
from schemas.notificacion import Notificacion
from schemas.notificacion_masiva import NotificacionMasiva

def save_notificacion(datos_notificacion: dict, db: SessionLocal):
  """
    Cambiar para que consiga estado e idCliente de otros subsistemas
  """
  datos_notificacion['fechaEnvio'] = datetime.now()
  datos_notificacion['estado'] = "finalizado"
  datos_notificacion['idCliente'] = 1

  notificacion = Notificacion.NotificacionCreate(**datos_notificacion)
  db_notificacion = Notificacion(**notificacion.dict())
  db.add(db_notificacion)
  db.commit()
  db.refresh(db_notificacion)
  return db_notificacion


def save_notificacion_masiva(datos_notificacion_masiva: dict, db: SessionLocal):
  datos_notificacion_masiva['fechaEnvio'] = datetime.now()

  notificacion_masiva = NotificacionMasiva.NotificacionMasivaCreate(**datos_notificacion_masiva)
  db_notificacion_masiva = NotificacionMasiva(**notificacion_masiva.dict())
  db.add(db_notificacion_masiva)
  db.commit()
  db.refresh(db_notificacion_masiva)
  return db_notificacion_masiva


def get_notificacion(idNotificacion: int, db: SessionLocal):
  notificacion = db.query(Notificacion).filter_by(idNotificacion=idNotificacion).first()
  return notificacion


def get_notificaciones_by_idTrabajo(idTrabajo: int, page: int, db: SessionLocal):
  page_size = 5
  offset = (page - 1) * page_size
  notificaciones = db.query(Notificacion).filter_by(idTrabajo=idTrabajo).limit(page_size).offset(offset).all()
  return notificaciones


def get_notificaciones_by_idCliente(idCliente: int, page: int, db: SessionLocal):
  page_size = 5
  offset = (page - 1) * page_size
  notificaciones = db.query(Notificacion).filter_by(idCliente=idCliente).limit(page_size).offset(offset).all()
  return notificaciones