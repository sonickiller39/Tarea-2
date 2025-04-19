from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.base_datos import Base, engine, SessionLocal
from app.modelos import Vuelo, EstadoVuelo
from app.vuelos import ListaVuelos
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

Base.metadata.create_all(bind=engine)

app = FastAPI()
lista_vuelos = ListaVuelos()  # Lista doblemente enlazada

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class VueloEntrada(BaseModel):
    codigo: str
    estado: EstadoVuelo
    hora: datetime
    origen: str
    destino: str

class VueloRespuesta(BaseModel):
    id: int
    codigo: str
    estado: EstadoVuelo
    hora: datetime
    origen: str
    destino: str

    class Config:
        orm_mode = True

# Vuelos existentes desde la bd
@app.on_event("startup")
def cargar_lista():
    db = SessionLocal()
    vuelos = db.query(Vuelo).all()
    for vuelo in vuelos:
        if vuelo.estado == EstadoVuelo.emergencia:
            lista_vuelos.insertar_al_frente(vuelo)
        else:
            lista_vuelos.insertar_al_final(vuelo)
    db.close()

@app.post("/vuelos", response_model=VueloRespuesta)
def agregar_vuelo(vuelo: VueloEntrada, db: Session = Depends(get_db)):
    vuelo_db = Vuelo(**vuelo.dict())
    db.add(vuelo_db)
    db.commit()
    db.refresh(vuelo_db)

    # Lista doblemente enlazada
    if vuelo_db.estado == EstadoVuelo.emergencia:
        lista_vuelos.insertar_al_frente(vuelo_db)
    else:
        lista_vuelos.insertar_al_final(vuelo_db)

    return vuelo_db

@app.get("/vuelos/total")
def total():
    return {"total": lista_vuelos.longitud()}

@app.get("/vuelos/proximo", response_model=Optional[VueloRespuesta])
def proximo():
    return lista_vuelos.obtener_primero()

@app.get("/vuelos/ultimo", response_model=Optional[VueloRespuesta])
def ultimo():
    return lista_vuelos.obtener_ultimo()

@app.get("/vuelos/lista", response_model=List[VueloRespuesta])
def listar():
    return lista_vuelos.recorrer()
