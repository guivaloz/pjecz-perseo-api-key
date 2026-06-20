"""
Puestos, modelos
"""

from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from pjecz_perseo_api_key.dependencies.database import Base
from pjecz_perseo_api_key.dependencies.universal_mixin import UniversalMixin


class Puesto(Base, UniversalMixin):
    """Puesto"""

    # Nombre de la tabla
    __tablename__ = "puestos"

    # Clave primaria
    id: Mapped[int] = mapped_column(primary_key=True)

    # Columnas
    clave: Mapped[str] = mapped_column(String(16), unique=True)
    descripcion: Mapped[str] = mapped_column(String(256))

    # Hijos
    tabuladores: Mapped[List["Tabulador"]] = relationship("Tabulador", back_populates="puesto")

    def __repr__(self):
        """Representación"""
        return f"<Puesto {self.clave}>"
