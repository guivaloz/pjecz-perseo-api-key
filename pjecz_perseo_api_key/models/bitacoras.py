"""
Bitácoras, modelos
"""

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from pjecz_perseo_api_key.dependencies.database import Base
from pjecz_perseo_api_key.dependencies.universal_mixin import UniversalMixin


class Bitacora(Base, UniversalMixin):
    """Bitácora"""

    # Nombre de la tabla
    __tablename__ = "bitacoras"

    # Clave primaria
    id: Mapped[int] = mapped_column(primary_key=True)

    # Claves foráneas
    modulo_id: Mapped[int] = mapped_column(ForeignKey("modulos.id"))
    modulo: Mapped["Modulo"] = relationship(back_populates="bitacoras")
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    usuario: Mapped["Usuario"] = relationship(back_populates="bitacoras")

    # Columnas
    descripcion: Mapped[str] = mapped_column(String(256))
    url: Mapped[str] = mapped_column(String(512))

    @property
    def modulo_nombre(self):
        """Nombre del módulo"""
        return self.modulo.nombre

    @property
    def usuario_email(self):
        """Email del usuario"""
        return self.usuario.email

    def __repr__(self):
        """Representación"""
        return f"<Bitácora {self.id}>"
