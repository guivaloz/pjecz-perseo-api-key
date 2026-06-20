"""
Bitacoras v4, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict


class BitacoraOut(BaseModel):
    """Esquema para entregar bitácoras"""

    id: int
    modulo_nombre: str
    usuario_email: str
    descripcion: str
    url: str
    model_config = ConfigDict(from_attributes=True)


class OneBitacoraOut(BaseModel):
    """Esquema para entregar una bitácora"""

    success: bool
    message: str
    data: BitacoraOut | None = None
