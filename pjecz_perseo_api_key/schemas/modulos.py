"""
Modulos v4, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict

from ..dependencies.schemas_base import OneBaseOut


class ModuloOut(BaseModel):
    """Esquema para entregar modulos"""

    id: int
    nombre: str
    nombre_corto: str
    icono: str
    ruta: str
    en_navegacion: bool
    model_config = ConfigDict(from_attributes=True)


class OneModuloOut(OneBaseOut):
    """Esquema para entregar un modulo"""

    data: ModuloOut | None = None
