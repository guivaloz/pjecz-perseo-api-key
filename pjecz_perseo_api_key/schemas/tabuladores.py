"""
Tabuladores v4, esquemas de pydantic
"""

from datetime import date

from pydantic import BaseModel, ConfigDict


class TabuladorOut(BaseModel):
    """Esquema para entregar tabuladores"""

    id: int
    puesto_id: int
    puesto_clave: str
    puesto_descripcion: str
    modelo: int
    nivel: int
    quinquenio: int
    fecha: date
    sueldo_base: float
    incentivo: float
    monedero: float
    rec_cul_dep: float
    sobresueldo: float
    rec_dep_cul_gravado: float
    rec_dep_cul_excento: float
    ayuda_transp: float
    monto_quinquenio: float
    total_percepciones: float
    salario_diario: float
    prima_vacacional_mensual: float
    aguinaldo_mensual: float
    prima_vacacional_mensual_adicional: float
    total_percepciones_integrado: float
    salario_diario_integrado: float
    model_config = ConfigDict(from_attributes=True)


class OneTabuladorOut(BaseModel):
    """Esquema para entregar un tabulador"""

    success: bool
    message: str
    data: TabuladorOut | None = None
