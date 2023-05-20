from datetime import date
from pydantic import BaseModel
from sqlalchemy import Column, Date, Integer, String
from schemas.database import Base

class Notificacion(Base):
  __tablename__ = 'notificaciones'

  idNotificacion = Column(Integer, primary_key=True, autoincrement=True)
  idTrabajo = Column(Integer)
  idCliente = Column(Integer)
  mensaje = Column(String)
  fechaEnvio = Column(Date)
  estado = Column(String)
  
  class NotificacionCreate(BaseModel):
    idTrabajo: int
    idCliente: int
    mensaje: str 
    fechaEnvio: date
    estado: str