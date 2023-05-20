from anyio import Path
from fastapi import Body, Depends, FastAPI, HTTPException, status, Query, Request
from schemas.database import SessionLocal, get_db
from schemas.notificacion import Notificacion
from schemas.notificacion_masiva import NotificacionMasiva
import notificaciones_service as notificaciones_service

app = FastAPI(
    title="Taller de Coches - Subsistema de Envío de Notificaciones",
    version="1.0.0",
)

@app.post("/notificaciones/correo")
async def enviar_notificacion_correo(request: Request, db: SessionLocal = Depends(get_db)):
  datos_notificacion = await request.json()
  if not datos_notificacion:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se proporcionaron datos de notificación.")
  # Enviando notificacion por correo...
  try:
    notificacion = notificaciones_service.save_notificacion(datos_notificacion=datos_notificacion, db=db)
  except Exception as e:
      raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
  
  enlaces = [
      {"rel": "self", "href": f"http://127.0.0.1:80/api/v1/notificaciones/1"},
      {"rel": "trabajo", "href": f"http://127.0.0.1:80/api/v1/trabajos/1"}
    ]
  notificacion.enlaces = enlaces
  return notificacion


@app.post("/notificaciones/telefono")
async def enviar_notificacion_telefono(request: Request, db: SessionLocal = Depends(get_db)):
  datos_notificacion = await request.json()
  if not datos_notificacion:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se proporcionaron datos de notificación.")
  # Enviando notificacion por telefono...
  try:
    notificacion = notificaciones_service.save_notificacion(datos_notificacion=datos_notificacion, db=db)
  except Exception as e:
      raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
  
  enlaces = [
      {"rel": "self", "href": f"http://127.0.0.1:80/api/v1/notificaciones/1"},
      {"rel": "trabajo", "href": f"http://127.0.0.1:80/api/v1/trabajos/1"}
    ]
  notificacion.enlaces = enlaces
  return notificacion


@app.post("/notificaciones/masivas")
async def enviar_notificacion_masiva(request: Request, db: SessionLocal = Depends(get_db)):
  datos_notificacion_masiva = await request.json()
  if not datos_notificacion_masiva:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se proporcionaron datos de notificación masiva.")
  try:
    notificacion_masiva = notificaciones_service.save_notificacion_masiva(datos_notificacion_masiva=datos_notificacion_masiva, db=db)
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))  
  return notificacion_masiva


@app.get("/notificaciones/{idNotificacion}")
async def obtener_notificacion(idNotificacion: int, db: SessionLocal = Depends(get_db)):
  if not idNotificacion:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se proporcionaron datos de notificación.")
  try:
    notificacion = notificaciones_service.get_notificacion(idNotificacion=idNotificacion, db=db)
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))  
  return notificacion


@app.get("/notificaciones/trabajo/{idTrabajo}")
async def obtener_notificaciones_trabajo(idTrabajo: int, page: int = Query(default=1, gt=0), db: SessionLocal = Depends(get_db)):
  if not idTrabajo:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se proporcionaron datos de notificación.")
  try:
    notificaciones = notificaciones_service.get_notificaciones_by_idTrabajo(idTrabajo=idTrabajo, page=page, db=db)
    if not notificaciones:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron notificaciones.")
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron notificaciones.")  
  return notificaciones
  

@app.get("/notificaciones/cliente/{idCliente}")
async def obtener_notificaciones_cliente(idCliente: int, page: int = Query(default=1, gt=0), db: SessionLocal = Depends(get_db)):
  if not idCliente:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se proporcionaron datos de notificación.")
  try:
    offset = page * 5
    notificaciones = notificaciones_service.get_notificaciones_by_idCliente(idCliente=idCliente, offset=offset, db=db)
    if not notificaciones:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron notificaciones.")
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron notificaciones.")  
  return notificaciones

@app.patch("/notificaciones/cliente/{idCliente}")
async def actualizar_suscripcion_notificaciones(idCliente: int, suscripcion: bool):
  """
    Por completar
  """
  if not idCliente and not suscripcion: 
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se proporcionaron datos suficientes.")
  try:
    cliente = notificaciones_service.change_suscripcion(idCliente=idCliente, suscripcion=suscripcion)
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))  
  return cliente