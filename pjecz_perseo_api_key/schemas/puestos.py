"""
Puestos v4, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict


class PuestoOut(BaseModel):
    """Esquema para entregar puestos"""

    id: int
    clave: str
    descripcion: str
    model_config = ConfigDict(from_attributes=True)


class OnePuestoOut(BaseModel):
    """Esquema para entregar un puesto"""

    success: bool
    message: str
    data: PuestoOut | None = None
