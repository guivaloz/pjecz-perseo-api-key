"""
Timbrados v4, esquemas de pydantic
"""

from datetime import date

from pydantic import BaseModel, ConfigDict


class TimbradoOut(BaseModel):
    """Esquema para entregar timbrados"""

    id: int
    nomina_id: int
    nomina_fecha_pago: date
    nomina_tipo: str
    persona_rfc: str
    persona_curp: str
    estado: str
    archivo_pdf: str
    url_pdf: str
    archivo_xml: str
    url_xml: str
    model_config = ConfigDict(from_attributes=True)


class OneTimbradoOut(BaseModel):
    """Esquema para entregar un timbrado"""

    success: bool
    message: str
    data: TimbradoOut | None = None
