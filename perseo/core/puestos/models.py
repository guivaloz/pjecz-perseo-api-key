"""
Puestos, modelos
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class Puesto(Base, UniversalMixin):
    """Puesto"""

    # Nombre de la tabla
    __tablename__ = "puestos"

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # Columnas
    clave = Column(String(16), unique=True, nullable=False)
    descripcion = Column(String(256), nullable=False)

    # Hijos
    tabuladores = relationship("Tabulador", back_populates="puesto")

    def __repr__(self):
        """Representación"""
        return f"<Puesto {self.clave}>"
