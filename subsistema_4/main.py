import hashlib
import json
from fastapi import Depends, FastAPI, HTTPException, Response, status, Query, Request
from schemas.database import SessionLocal, get_db
import notificaciones_service as notificaciones_service
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Taller de Coches - Subsistema de Envío de Notificaciones",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/notificaciones/correo")
async def enviar_notificacion_correo(request: Request, db: SessionLocal = Depends(get_db)):
  try:
    datos_notificacion = await request.json()
    notificacion = notificaciones_service.save_notificacion(datos_notificacion=datos_notificacion, db=db)
  except json.JSONDecodeError:
    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=create_error_response(422, "Missing field"))
  except Exception:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=create_error_response(400, "Bad syntax"))
  
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
  try:
    datos_notificacion = await request.json()
    notificacion = notificaciones_service.save_notificacion(datos_notificacion=datos_notificacion, db=db)
  except json.JSONDecodeError:
    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=create_error_response(422, "Missing field"))
  except Exception:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=create_error_response(400, "Bad syntax"))
  
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
  try:
    datos_notificacion_masiva = await request.json()
    notificacion_masiva = notificaciones_service.save_notificacion_masiva(datos_notificacion_masiva=datos_notificacion_masiva, db=db)
  except json.JSONDecodeError:
    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=create_error_response(422, "Missing field"))
  #except Exception:
  #  raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=create_error_response(400, "Bad syntax"))
  
  return notificacion_masiva

@app.options("/notificaciones/masivas")
def notificaciones_masivas_options():
  allowed_methods = ["POST"]
  return {"allow": allowed_methods}



@app.get("/notificaciones/{idNotificacion}")
async def obtener_notificacion(idNotificacion: int, response: Response, db: SessionLocal = Depends(get_db)):
  if not idNotificacion:
    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=create_error_response(422, "Missing field"))
  
  try:
    notificacion = notificaciones_service.get_notificacion(idNotificacion=idNotificacion, db=db)
  except Exception:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=create_error_response(400, "Resource not found"))  
  
  enlaces = [
    {"rel": "self", "href": f"http://127.0.0.1:80/api/v1/notificaciones/1"},
    {"rel": "trabajo", "href": f"http://127.0.0.1:80/api/v1/trabajos/1"}
  ]
  notificacion.enlaces = enlaces
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
    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=create_error_response(422, "Missing field"))
  
  try:
    notificaciones = notificaciones_service.get_notificaciones_by_idTrabajo(idTrabajo=idTrabajo, page=page, db=db)
    if not notificaciones:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=create_error_response(404, "Resource not found"))  
  
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
    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=create_error_response(422, "Missing field"))
  
  try:
    notificaciones = notificaciones_service.get_notificaciones_by_idCliente(idCliente=idCliente, page=page, db=db)
    if not notificaciones:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=create_error_response(404, "Resource not found"))  
  
  notificaciones_str = str(notificaciones)
  etag = hashlib.md5(notificaciones_str.encode()).hexdigest()
  response.headers["ETag"] = etag
  return notificaciones

@app.patch("/notificaciones/cliente/{idCliente}")
async def actualizar_suscripcion_notificaciones(idCliente: int, request: Request, db: SessionLocal = Depends(get_db)):
  try:
    if not idCliente:
      raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=create_error_response(422, "Missing field"))
    
    datos_cliente = await request.json()
    cliente = notificaciones_service.change_suscripcion(idCliente=idCliente, suscripcion=datos_cliente["suscripcion"], db=db)
  except json.JSONDecodeError:
    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=create_error_response(422, "Missing field"))  
  except Exception as e:
    raise e
  
  return jsonable_encoder(cliente)

@app.options("/notificaciones/cliente/{idNotificacion}")
def notificaciones_idCliente_options():
  allowed_methods = ["GET", "PATCH"]
  return {"allow": allowed_methods}



def create_error_response(status_code: int, detail: str):
  error_response = {
    "type": f"https://httpstatuses.com/{status_code}",
    "title": "UNPROCESSABLE ENTITY",
    "status": status_code,
    "detail": detail,
    "instance": "about:blank"
  }
  return error_response