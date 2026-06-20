"""
Permisos v4, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict


class PermisoOut(BaseModel):
    """Esquema para entregar permisos"""

    id: int
    rol_id: int
    rol_nombre: str
    modulo_id: int
    modulo_nombre: str
    nivel: int
    nombre: str
    model_config = ConfigDict(from_attributes=True)


class OnePermisoOut(BaseModel):
    """Esquema para entregar un permiso"""

    success: bool
    message: str
    data: PermisoOut | None = None
