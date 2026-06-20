"""
Nóminas, modelos
"""

from datetime import date
from decimal import Decimal, getcontext
from typing import List, Optional

from sqlalchemy import Enum, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from pjecz_perseo_api_key.dependencies.database import Base
from pjecz_perseo_api_key.dependencies.universal_mixin import UniversalMixin

getcontext().prec = 4  # Cuatro decimales en los cálculos monetarios


class Nomina(Base, UniversalMixin):
    """Nómina"""

    TIPOS = {
        "AGUINALDO": "AGUINALDO",
        "APOYO ANUAL": "APOYO ANUAL",
        "APOYO DIA DE LA MADRE": "APOYO DIA DE LA MADRE",
        "ASIMILADO": "ASIMILADO",
        "DESPENSA": "DESPENSA",
        "EXTRAORDINARIO": "EXTRAORDINARIO",
        "PENSION ALIMENTICIA": "PENSION ALIMENTICIA",
        "PRIMA VACACIONAL": "PRIMA VACACIONAL",
        "SALARIO": "SALARIO",
        "RETROACTIVO AGUINALDO": "RETROACTIVO AGUINALDO",
    }

    # Nombre de la tabla
    __tablename__ = "nominas"

    # Clave primaria
    id: Mapped[int] = mapped_column(primary_key=True)

    # Clave foránea
    persona_id: Mapped[int] = mapped_column(ForeignKey("personas.id"))
    persona: Mapped["Persona"] = relationship(back_populates="nominas")

    # Columnas
    tipo: Mapped[str] = mapped_column(Enum(*TIPOS, name="nominas_tipos"), index=True)
    desde: Mapped[date]
    desde_clave: Mapped[str] = mapped_column(String(6))
    hasta: Mapped[date]
    hasta_clave: Mapped[str] = mapped_column(String(6))
    percepcion: Mapped[Decimal] = mapped_column(Numeric(precision=24, scale=4))
    deduccion: Mapped[Decimal] = mapped_column(Numeric(precision=24, scale=4))
    importe: Mapped[Decimal] = mapped_column(Numeric(precision=24, scale=4))
    num_cheque: Mapped[str] = mapped_column(String(24), default="", server_default="")
    fecha_pago: Mapped[date]
    timbrado_id: Mapped[Optional[int]] = mapped_column(Integer(), nullable=True)

    # Hijos
    timbrados: Mapped[List["Timbrado"]] = relationship("Timbrado", back_populates="nomina")

    @property
    def persona_curp(self):
        """CURP de la persona"""
        return self.persona.curp

    @property
    def persona_rfc(self):
        """RFC de la persona"""
        return self.persona.rfc

    def __repr__(self):
        """Representación"""
        return f"<Nómina {self.id}>"
