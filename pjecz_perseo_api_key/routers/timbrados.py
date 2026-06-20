"""
Timbrados
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from pjecz_perseo_api_key.dependencies.authentications import UsuarioInDB, get_current_active_user
from pjecz_perseo_api_key.dependencies.database import Session, get_db
from pjecz_perseo_api_key.dependencies.fastapi_pagination_custom_page import CustomPage
from pjecz_perseo_api_key.dependencies.safe_string import safe_curp, safe_rfc
from pjecz_perseo_api_key.models.nominas import Nomina
from pjecz_perseo_api_key.models.permisos import Permiso
from pjecz_perseo_api_key.models.personas import Persona
from pjecz_perseo_api_key.models.timbrados import Timbrado
from pjecz_perseo_api_key.schemas.timbrados import TimbradoOut

timbrados = APIRouter(prefix="/api/v5/timbrados", tags=["timbrados"])


@timbrados.get("", response_model=CustomPage[TimbradoOut])
async def paginado_timbrados(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    curp: str | None = None,
    rfc: str | None = None,
):
    """Paginado de timbrados"""
    if current_user.permissions.get("TIMBRADOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    consulta = database.query(Timbrado)
    if curp is not None:
        try:
            curp = safe_curp(curp, search_fragment=True)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No es válido el CURP")
        consulta = consulta.join(Nomina).join(Persona).filter(Persona.curp == curp).filter(Persona.estatus == "A")
    elif rfc is not None:
        try:
            rfc = safe_rfc(rfc)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No es válido el RFC")
        consulta = consulta.join(Nomina).join(Persona).filter(Persona.rfc == rfc).filter(Persona.estatus == "A")
    return paginate(consulta.filter(Timbrado.estatus == "A").order_by(Timbrado.id.desc()))
