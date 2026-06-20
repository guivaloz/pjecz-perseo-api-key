"""
Tareas v4, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict


class TareaOut(BaseModel):
    """Esquema para entregar tareas"""

    id: str  # El id es string y es el mismo que usa el RQ worker
    usuario_id: int
    usuario_email: str
    comando: str
    mensaje: str
    ha_terminado: bool
    model_config = ConfigDict(from_attributes=True)


class OneTareaOut(BaseModel):
    """Esquema para entregar un tarea"""

    success: bool
    message: str
    data: TareaOut | None = None
