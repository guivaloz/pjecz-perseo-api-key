"""
Personas, modelos
"""

from datetime import date
from typing import List, Optional

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..dependencies.database import Base
from ..dependencies.universal_mixin import UniversalMixin


class Persona(Base, UniversalMixin):
    """Persona"""

    MODELOS = {
        1: "CONFIANZA",
        2: "SINDICALIZADO",
        3: "PENSIONADO",
        4: "BENEFICIARIO PENSION ALIMENTICIA",
        5: "ASIMILADO A SALARIOS",
        6: "EXTRAORDINARIO",
    }

    # Nombre de la tabla
    __tablename__ = "personas"

    # Clave primaria
    id: Mapped[int] = mapped_column(primary_key=True)

    # Clave foránea
    tabulador_id: Mapped[int] = mapped_column(ForeignKey("tabuladores.id"))
    tabulador: Mapped["Tabulador"] = relationship(back_populates="personas")

    # Columnas
    rfc: Mapped[str] = mapped_column(String(13), unique=True, index=True)
    nombres: Mapped[str] = mapped_column(String(256), index=True)
    apellido_primero: Mapped[str] = mapped_column(String(256), index=True)
    apellido_segundo: Mapped[str] = mapped_column(String(256), default="", server_default="")
    curp: Mapped[str] = mapped_column(String(18), default="", server_default="")
    num_empleado: Mapped[Optional[int]]
    ingreso_gobierno_fecha: Mapped[Optional[date]]
    ingreso_pj_fecha: Mapped[Optional[date]]
    nacimiento_fecha: Mapped[Optional[date]]
    codigo_postal_fiscal: Mapped[Optional[int]] = mapped_column(Integer, default=0)
    seguridad_social: Mapped[Optional[str]] = mapped_column(String(24))

    # Columna modelo es entero del 1 al 6
    modelo: Mapped[int] = mapped_column(Integer, index=True)

    # Columnas para mantener el ultimo centro_trabajo, plaza y puesto
    # que se actualizan cada vez que se alimiente una quincena
    ultimo_centro_trabajo_id: Mapped[int] = mapped_column(Integer, default=137)
    ultimo_plaza_id: Mapped[int] = mapped_column(Integer, default=2182)
    ultimo_puesto_id: Mapped[int] = mapped_column(Integer, default=135)

    # Columnas para sindicalizados
    sub_sis: Mapped[int] = mapped_column(Integer, default=0)
    nivel: Mapped[int] = mapped_column(Integer, default=0)
    puesto_equivalente: Mapped[str] = mapped_column(String(16), default="")

    # Hijos
    nominas: Mapped[List["Nomina"]] = relationship("Nomina", back_populates="persona")

    @property
    def nombre_completo(self):
        """Nombre completo"""
        return f"{self.nombres} {self.apellido_primero} {self.apellido_segundo}"

    def __repr__(self):
        """Representación"""
        return f"<Persona {self.rfc}>"
