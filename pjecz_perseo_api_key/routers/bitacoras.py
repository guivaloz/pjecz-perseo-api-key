"""
Bitácoras
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from pjecz_perseo_api_key.dependencies.authentications import UsuarioInDB, get_current_active_user
from pjecz_perseo_api_key.dependencies.database import Session, get_db
from pjecz_perseo_api_key.dependencies.fastapi_pagination_custom_page import CustomPage
from pjecz_perseo_api_key.dependencies.safe_string import safe_email
from pjecz_perseo_api_key.models.bitacoras import Bitacora
from pjecz_perseo_api_key.models.modulos import Modulo
from pjecz_perseo_api_key.models.permisos import Permiso
from pjecz_perseo_api_key.models.usuarios import Usuario
from pjecz_perseo_api_key.schemas.bitacoras import BitacoraOut

bitacoras = APIRouter(prefix="/api/v5/bitacoras", tags=["usuarios"])


@bitacoras.get("", response_model=CustomPage[BitacoraOut])
async def paginado_bitacoras(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    modulo_id: int | None = None,
    email: str | None = None,
):
    """Paginado de bitácoras"""
    if current_user.permissions.get("BITACORAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    consulta = database.query(Bitacora)
    if modulo_id is not None:
        consulta = consulta.join(Modulo).filter(Modulo.id == modulo_id).filter(Modulo.estatus == "A")
    if email is not None:
        try:
            email = safe_email(email)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No es válido el e-mail")
        consulta = consulta.join(Usuario).filter(Usuario.email == email).filter(Usuario.estatus == "A")
    return paginate(consulta.filter(Bitacora.estatus == "A").order_by(Bitacora.id.desc()))
