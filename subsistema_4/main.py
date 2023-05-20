import hashlib
import json
from fastapi import Depends, FastAPI, HTTPException, Response, status, Query, Request
from schemas.database import SessionLocal, get_db
import notificaciones_service as notificaciones_service

app = FastAPI(
    title="Taller de Coches - Subsistema de Envío de Notificaciones",
    version="1.0.0",
)

@app.post("/notificaciones/correo")
async def enviar_notificacion_correo(request: Request, db: SessionLocal = Depends(get_db)):
  datos_notificacion = await request.json()
  if not datos_notificacion or datos_notificacion.get("idTrabajo") is None or datos_notificacion.get("mensaje") is None:
    error_response = {
      "type": "https://httpstatuses.com/400",
      "title": "UNPROCESSABLE ENTITY",
      "status": 400,
      "detail": "Malformed Syntax",
      "instance": "about:blank"
    }
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_response)
  
  # ...Enviando notificacion por correo...
  
  try:
    notificacion = notificaciones_service.save_notificacion(datos_notificacion=datos_notificacion, db=db)
  except Exception as e:
    error_response = {
      "type": "https://httpstatuses.com/422",
      "title": "UNPROCESSABLE ENTITY",
      "status": 422,
      "detail": "Unprocessable Entity",
      "instance": "about:blank"
    }
    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=error_response)
  
  enlaces = [
    {"rel": "self", "href": f"http://127.0.0.1:80/api/v1/notificaciones/1"},
    {"rel": "trabajo", "href": f"http://127.0.0.1:80/api/v1/trabajos/1"}
  ]
  notificacion.enlaces = enlaces
  return notificacion

@app.options("/notificaciones/correo")
def notificaciones_correo_options():
  allowed_methods = ["POST"]
  return {"allow": allowed_methods}

@app.post("/notificaciones/telefono")
async def enviar_notificacion_telefono(request: Request, db: SessionLocal = Depends(get_db)):
  datos_notificacion = await request.json()
  if not datos_notificacion or datos_notificacion.get("idTrabajo") is None or datos_notificacion.get("mensaje") is None:
    error_response = {
      "type": "https://httpstatuses.com/400",
      "title": "UNPROCESSABLE ENTITY",
      "status": 400,
      "detail": "Malformed Syntax",
      "instance": "about:blank"
    }
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_response)
  
  # ...Enviando notificacion por telefono...

  try:
    notificacion = notificaciones_service.save_notificacion(datos_notificacion=datos_notificacion, db=db)
  except Exception as e:
    error_response = {
      "type": "https://httpstatuses.com/422",
      "title": "UNPROCESSABLE ENTITY",
      "status": 422,
      "detail": "Unprocessable Entity",
      "instance": "about:blank"
    }
    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=error_response)
  
  enlaces = [
      {"rel": "self", "href": f"http://127.0.0.1:80/api/v1/notificaciones/1"},
      {"rel": "trabajo", "href": f"http://127.0.0.1:80/api/v1/trabajos/1"}
    ]
  notificacion.enlaces = enlaces
  return notificacion

@app.options("/notificaciones/telefono")
def notificaciones_telefono_options():
  allowed_methods = ["POST"]
  return {"allow": allowed_methods}

@app.post("/notificaciones/masivas")
async def enviar_notificacion_masiva(request: Request, db: SessionLocal = Depends(get_db)):
  datos_notificacion_masiva = await request.json()
  if not datos_notificacion_masiva:
    error_response = {
      "type": "https://httpstatuses.com/400",
      "title": "UNPROCESSABLE ENTITY",
      "status": 400,
      "detail": "Malformed Syntax",
      "instance": "about:blank"
    }
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_response)
  
  try:
    notificacion_masiva = notificaciones_service.save_notificacion_masiva(datos_notificacion_masiva=datos_notificacion_masiva, db=db)
  except Exception as e:
    error_response = {
      "type": "https://httpstatuses.com/422",
      "title": "UNPROCESSABLE ENTITY",
      "status": 422,
      "detail": "Unprocessable Entity",
      "instance": "about:blank"
    }
    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=error_response)
  return notificacion_masiva

@app.options("/notificaciones/masivas")
def notificaciones_masivas_options():
  allowed_methods = ["POST"]
  return {"allow": allowed_methods}

@app.get("/notificaciones/{idNotificacion}")
async def obtener_notificacion(idNotificacion: int, response: Response, db: SessionLocal = Depends(get_db)):
  if not idNotificacion:
    error_response = {
      "type": "https://httpstatuses.com/400",
      "title": "UNPROCESSABLE ENTITY",
      "status": 400,
      "detail": "Malformed Syntax",
      "instance": "about:blank"
    }
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_response)
  try:
    notificacion = notificaciones_service.get_notificacion(idNotificacion=idNotificacion, db=db)
  except Exception as e:
    error_response = {
      "type": "https://httpstatuses.com/404",
      "title": "NOT FOUND",
      "status": 404,
      "detail": "Resource not found",
      "instance": "about:blank"
    }
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error_response)  
  
  notificacion_str = str(notificacion)
  etag = hashlib.md5(notificacion_str.encode()).hexdigest()
  response.headers["ETag"] = etag
  return notificacion

@app.options("/notificaciones/{idNotificacion}")
def notificaciones_idNotificacion_options():
  allowed_methods = ["GET"]
  return {"allow": allowed_methods}

@app.get("/notificaciones/trabajo/{idTrabajo}")
async def obtener_notificaciones_trabajo(response: Response, idTrabajo: int, page: int = Query(default=1, gt=0), db: SessionLocal = Depends(get_db)):
  if not idTrabajo:
    error_response = {
      "type": "https://httpstatuses.com/400",
      "title": "UNPROCESSABLE ENTITY",
      "status": 400,
      "detail": "Malformed Syntax",
      "instance": "about:blank"
    }
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_response)
  try:
    notificaciones = notificaciones_service.get_notificaciones_by_idTrabajo(idTrabajo=idTrabajo, page=page, db=db)
    if not notificaciones:
      error_response = {
        "type": "https://httpstatuses.com/404",
        "title": "NOT FOUND",
        "status": 404,
        "detail": "Resource not found",
        "instance": "about:blank"
      }
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error_response)  
  except Exception as e:
    raise e
  
  notificaciones_str = str(notificaciones)
  etag = hashlib.md5(notificaciones_str.encode()).hexdigest()
  response.headers["ETag"] = etag
  return notificaciones

@app.options("/notificaciones/trabajo/{idTrabajo}")
def notificaciones_idTrabajo_options():
  allowed_methods = ["GET"]
  return {"allow": allowed_methods}

@app.get("/notificaciones/cliente/{idCliente}")
async def obtener_notificaciones_cliente(response: Response, idCliente: int, page: int = Query(default=1, gt=0), db: SessionLocal = Depends(get_db)):
  if not idCliente:
    error_response = {
      "type": "https://httpstatuses.com/400",
      "title": "UNPROCESSABLE ENTITY",
      "status": 400,
      "detail": "Malformed Syntax",
      "instance": "about:blank"
    }
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_response)
  try:
    notificaciones = notificaciones_service.get_notificaciones_by_idCliente(idCliente=idCliente, page=page, db=db)
    if not notificaciones:
      error_response = {
        "type": "https://httpstatuses.com/404",
        "title": "NOT FOUND",
        "status": 404,
        "detail": "Resource not found",
        "instance": "about:blank"
      }
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error_response)  
  except Exception as e:
    raise e
  
  notificaciones_str = str(notificaciones)
  etag = hashlib.md5(notificaciones_str.encode()).hexdigest()
  response.headers["ETag"] = etag
  return notificaciones

@app.patch("/notificaciones/cliente/{idCliente}")
async def actualizar_suscripcion_notificaciones(idCliente: int, suscripcion: bool):
  """
    Por completar
  """
  if not idCliente and not suscripcion: 
    error_response = {
      "type": "https://httpstatuses.com/400",
      "title": "UNPROCESSABLE ENTITY",
      "status": 400,
      "detail": "Malformed Syntax",
      "instance": "about:blank"
    }
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_response)
  try:
    cliente = notificaciones_service.change_suscripcion(idCliente=idCliente, suscripcion=suscripcion)
  except Exception as e:
    error_response = {
      "type": "https://httpstatuses.com/404",
      "title": "NOT FOUND",
      "status": 404,
      "detail": "Resource not found",
      "instance": "about:blank"
    }
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error_response) 
  return cliente

@app.options("/notificaciones/cliente/{idNotificacion}")
def notificaciones_idCliente_options():
  allowed_methods = ["GET", "PATCH"]
  return {"allow": allowed_methods}