from sqlalchemy import Column, Integer, String, Enum, DateTime
from app.base_datos import Base
import enum

class EstadoVuelo(enum.Enum):
    programado = "programado"
    emergencia = "emergencia"
    retrasado = "retrasado"

class Vuelo(Base):
    __tablename__ = "vuelos"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, unique=True, nullable=False)
    estado = Column(Enum(EstadoVuelo), nullable=False)
    hora = Column(DateTime, nullable=False)
    origen = Column(String, nullable=False)
    destino = Column(String, nullable=False)
