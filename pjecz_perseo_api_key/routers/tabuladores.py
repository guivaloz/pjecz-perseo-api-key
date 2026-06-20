"""
Tabuladores
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from pjecz_perseo_api_key.dependencies.authentications import UsuarioInDB, get_current_active_user
from pjecz_perseo_api_key.dependencies.database import Session, get_db
from pjecz_perseo_api_key.dependencies.fastapi_pagination_custom_page import CustomPage
from pjecz_perseo_api_key.dependencies.safe_string import safe_clave
from pjecz_perseo_api_key.models.permisos import Permiso
from pjecz_perseo_api_key.models.puestos import Puesto
from pjecz_perseo_api_key.models.tabuladores import Tabulador
from pjecz_perseo_api_key.schemas.tabuladores import TabuladorOut

tabuladores = APIRouter(prefix="/api/v5/tabuladores", tags=["tabuladores"])


@tabuladores.get("", response_model=CustomPage[TabuladorOut])
async def paginado_tabuladores(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    puesto_clave: str | None = None,
):
    """Paginado de tabuladores"""
    if current_user.permissions.get("TABULADORES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    consulta = database.query(Tabulador)
    if puesto_clave is not None:
        try:
            puesto_clave = safe_clave(puesto_clave)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No es válida la clave del distrito")
        consulta = consulta.join(Puesto).filter(Puesto.clave == puesto_clave).filter(Puesto.estatus == "A")
    return paginate(consulta.filter(Tabulador.estatus == "A").order_by(Tabulador.id))
