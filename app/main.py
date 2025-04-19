from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.modelos import Vuelo, EstadoVuelo
from app.vuelos import ListaVuelos
from app.base_datos import Base, engine, SessionLocal
from pydantic import BaseModel
from datetime import datetime

Base.metadata.create_all(bind=engine)

app = FastAPI()
lista_vuelos = ListaVuelos()

class VueloEntrada(BaseModel):
    codigo: str
    estado: EstadoVuelo
    hora: datetime
    origen: str
    destino: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/vuelos")
def agregar_vuelo(vuelo: VueloEntrada, db: Session = Depends(get_db)):
    vuelo_db = Vuelo(**vuelo.dict())
    db.add(vuelo_db)
    db.commit()
    db.refresh(vuelo_db)

    if vuelo.estado == EstadoVuelo.emergencia:
        lista_vuelos.insertar_al_frente(vuelo_db)
    else:
        lista_vuelos.insertar_al_final(vuelo_db)
    return {"mensaje": "Vuelo agregado."}

@app.get("/vuelos/total")
def total():
    return {"total": lista_vuelos.longitud()}

@app.get("/vuelos/proximo")
def proximo():
    return lista_vuelos.obtener_primero()

@app.get("/vuelos/ultimo")
def ultimo():
    return lista_vuelos.obtener_ultimo()

@app.get("/vuelos/lista")
def listar():
    return lista_vuelos.recorrer()
