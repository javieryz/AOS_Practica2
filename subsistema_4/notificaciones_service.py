from datetime import datetime
from fastapi import HTTPException, status
from schemas.database import SessionLocal
from schemas.notificacion import Notificacion
from schemas.notificacion_masiva import NotificacionMasiva
from schemas.cliente import Cliente

def save_notificacion(datos_notificacion: dict, db: SessionLocal):
  datos_notificacion['fechaEnvio'] = datetime.now()
  """
    En la implementación completa, estado e idCliente se obtendrían con una petición al microservicio de Clientes
  """
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


def change_suscripcion(idCliente: int, suscripcion: bool, db: SessionLocal):
  cliente = db.query(Cliente).filter_by(idCliente=idCliente).first()
  if cliente:
    cliente.recibeNotificaciones = suscripcion
    db.commit()
    print(cliente.idCliente)
    return cliente
  else:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)