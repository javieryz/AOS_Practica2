from pydantic import BaseModel
from sqlalchemy import Boolean, Column, Integer, String
from schemas.database import Base

class Cliente(Base):
  __tablename__ = 'clientes'

  idCliente = Column(Integer, primary_key=True)
  nombre = Column(String)
  apellido = Column(String)
  telefono = Column(Integer)
  email = Column(String)
  direccion = Column(String)
  recibeNotificaciones = Column(Boolean)

  class ClienteCreate(BaseModel):
    nombre: str
    apellido: str
    telefono: int
    email: str
    direccion: str
    recibeNotificaciones: bool