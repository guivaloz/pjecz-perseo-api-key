"""
Entradas-Salidas
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from pjecz_perseo_api_key.dependencies.authentications import UsuarioInDB, get_current_active_user
from pjecz_perseo_api_key.dependencies.database import Session, get_db
from pjecz_perseo_api_key.dependencies.fastapi_pagination_custom_page import CustomPage
from pjecz_perseo_api_key.dependencies.safe_string import safe_email
from pjecz_perseo_api_key.models.entradas_salidas import EntradaSalida
from pjecz_perseo_api_key.models.permisos import Permiso
from pjecz_perseo_api_key.models.usuarios import Usuario
from pjecz_perseo_api_key.schemas.entradas_salidas import EntradaSalidaOut

entradas_salidas = APIRouter(prefix="/api/v5/entradas_salidas", tags=["usuarios"])


@entradas_salidas.get("", response_model=CustomPage[EntradaSalidaOut])
async def paginado_entradas_salidas(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    email: str | None = None,
):
    """Paginado de entradas-salidas"""
    if current_user.permissions.get("ENTRADAS SALIDAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    consulta = database.query(EntradaSalida)
    if email is not None:
        try:
            email = safe_email(email)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No es válido el e-mail")
        consulta = consulta.join(Usuario).filter(Usuario.email == email).filter(Usuario.estatus == "A")
    return paginate(consulta.filter(EntradaSalida.estatus == "A").order_by(EntradaSalida.id.desc()))
