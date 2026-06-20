"""
Personas v4, esquemas de pydantic
"""

from datetime import date

from pydantic import BaseModel, ConfigDict


class PersonaOut(BaseModel):
    """Esquema para entregar personas"""

    id: int
    tabulador_id: int
    rfc: str
    nombres: str
    apellido_primero: str
    apellido_segundo: str
    curp: str
    num_empleado: int | None
    ingreso_gobierno_fecha: date | None
    ingreso_pj_fecha: date | None
    nacimiento_fecha: date | None
    codigo_postal_fiscal: int | None
    seguridad_social: str | None
    modelo: int
    nombre_completo: str
    model_config = ConfigDict(from_attributes=True)


class OnePersonaOut(BaseModel):
    """Esquema para entregar una persona"""

    success: bool
    message: str
    data: PersonaOut | None = None
