from datetime import date
from pydantic import BaseModel
from sqlalchemy import Column, Date, Integer, String
from schemas.database import Base

class NotificacionMasiva(Base):
  __tablename__ = 'notificaciones_masivas'

  idNotificacion = Column(Integer, primary_key=True)
  mensaje = Column(String)
  fechaEnvio = Column(Date)

  class NotificacionMasivaCreate(BaseModel):
    mensaje: str
    fechaEnvio: date