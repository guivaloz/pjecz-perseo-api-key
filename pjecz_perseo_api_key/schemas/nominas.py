"""
Nominas v4, esquemas de pydantic
"""

from datetime import date

from pydantic import BaseModel, ConfigDict


class NominaOut(BaseModel):
    """Esquema para entregar nominas"""

    id: int
    persona_id: int
    persona_curp: str
    persona_rfc: str
    fecha_pago: date
    tipo: str
    timbrado_id: int
    model_config = ConfigDict(from_attributes=True)


class OneNominaOut(BaseModel):
    """Esquema para entregar una nomina"""

    success: bool
    message: str
    data: NominaOut | None = None
