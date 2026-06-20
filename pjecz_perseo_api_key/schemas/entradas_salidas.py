"""
Entradas-Salidas v4, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict


class EntradaSalidaOut(BaseModel):
    """Esquema para entregar entradas-salidas"""

    id: int
    usuario_email: str
    tipo: str
    direccion_ip: str
    model_config = ConfigDict(from_attributes=True)


class OneEntradaSalidaOut(BaseModel):
    """Esquema para entregar una entrada-salida"""

    success: bool
    message: str
    data: EntradaSalidaOut | None = None
