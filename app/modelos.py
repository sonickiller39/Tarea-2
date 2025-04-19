from sqlalchemy import Column, String, Enum, DateTime
from app.base_datos import Base
import enum

class EstadoVuelo(enum.Enum):
    programado = "programado"
    emergencia = "emergencia"
    retrasado = "retrasado"

class Vuelo(Base):
    __tablename__ = "vuelos"
    codigo = Column(String, primary_key=True, index=True)
    estado = Column(Enum(EstadoVuelo))
    hora = Column(DateTime)
    origen = Column(String)
    destino = Column(String)
