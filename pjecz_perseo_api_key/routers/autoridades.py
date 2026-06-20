"""
Autoridades
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.exc import MultipleResultsFound, NoResultFound

from pjecz_perseo_api_key.dependencies.authentications import UsuarioInDB, get_current_active_user
from pjecz_perseo_api_key.dependencies.database import Session, get_db
from pjecz_perseo_api_key.dependencies.fastapi_pagination_custom_page import CustomPage
from pjecz_perseo_api_key.dependencies.safe_string import safe_clave
from pjecz_perseo_api_key.models.autoridades import Autoridad
from pjecz_perseo_api_key.models.distritos import Distrito
from pjecz_perseo_api_key.models.permisos import Permiso
from pjecz_perseo_api_key.schemas.autoridades import AutoridadOut, OneAutoridadOut

autoridades = APIRouter(prefix="/api/v5/autoridades", tags=["autoridades"])


@autoridades.get("/{clave}", response_model=OneAutoridadOut)
async def detalle_autoridad(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    clave: str,
):
    """Detalle de una autoridad a partir de su clave"""
    if current_user.permissions.get("AUTORIDADES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        clave = safe_clave(clave)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No es válida la clave")
    try:
        autoridad = database.query(Autoridad).filter_by(clave=clave).one()
    except MultipleResultsFound, NoResultFound:
        return OneAutoridadOut(success=False, message="No existe esa autoridad")
    if autoridad.estatus != "A":
        return OneAutoridadOut(success=False, message="No está habilitado esa autoridad")
    return OneAutoridadOut(success=True, message=f"Detalle de {clave}", data=AutoridadOut.model_validate(autoridad))


@autoridades.get("", response_model=CustomPage[AutoridadOut])
async def paginado_autoridades(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    distrito_clave: str | None = None,
    es_extinto: bool | None = None,
):
    """Paginado de autoridades"""
    if current_user.permissions.get("AUTORIDADES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    consulta = database.query(Autoridad)
    if distrito_clave is not None:
        try:
            distrito_clave = safe_clave(distrito_clave)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No es válida la clave del distrito")
        consulta = consulta.join(Distrito).filter(Distrito.clave == distrito_clave).filter(Distrito.estatus == "A")
    if es_extinto is not None:
        consulta = consulta.filter(Autoridad.es_extinto == es_extinto)
    return paginate(consulta.filter(Autoridad.estatus == "A").order_by(Autoridad.clave))
