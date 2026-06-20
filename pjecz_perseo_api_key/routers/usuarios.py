"""
Usuarios
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.exc import MultipleResultsFound, NoResultFound

from pjecz_perseo_api_key.dependencies.authentications import UsuarioInDB, get_current_active_user
from pjecz_perseo_api_key.dependencies.database import Session, get_db
from pjecz_perseo_api_key.dependencies.fastapi_pagination_custom_page import CustomPage
from pjecz_perseo_api_key.dependencies.safe_string import safe_clave, safe_email, safe_string
from pjecz_perseo_api_key.models.autoridades import Autoridad
from pjecz_perseo_api_key.models.permisos import Permiso
from pjecz_perseo_api_key.models.usuarios import Usuario
from pjecz_perseo_api_key.schemas.usuarios import OneUsuarioOut, UsuarioOut

usuarios = APIRouter(prefix="/api/v5/usuarios", tags=["usuarios"])


@usuarios.get("/{email}", response_model=OneUsuarioOut)
async def detalle_usuario(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    email: str,
):
    """Detalle de un usuario a partir de su e-mail"""
    if current_user.permissions.get("USUARIOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        email = safe_email(email)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No es válido el e-mail")
    try:
        usuario = database.query(Usuario).filter_by(email=email).one()
    except MultipleResultsFound, NoResultFound:
        return OneUsuarioOut(success=False, message="No existe ese usuario")
    if usuario.estatus != "A":
        return OneUsuarioOut(success=False, message="No está habilitado ese usuario")
    return OneUsuarioOut(success=True, message=f"Detalle de {email}", data=UsuarioOut.model_validate(usuario))


@usuarios.get("", response_model=CustomPage[UsuarioOut])
async def paginado_usuarios(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    apellido_primero: str | None = None,
    apellido_segundo: str | None = None,
    autoridad_clave: str | None = None,
    email: str | None = None,
    nombres: str | None = None,
):
    """Paginado de usuarios"""
    if current_user.permissions.get("USUARIOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    consulta = database.query(Usuario)
    if apellido_primero is not None:
        apellido_primero = safe_string(apellido_primero)
        if apellido_primero != "":
            consulta = consulta.filter(Usuario.apellido_primero.contains(apellido_primero))
    if apellido_segundo is not None:
        apellido_segundo = safe_string(apellido_segundo)
        if apellido_segundo != "":
            consulta = consulta.filter(Usuario.apellido_segundo.contains(apellido_segundo))
    if autoridad_clave is not None:
        try:
            autoridad_clave = safe_clave(autoridad_clave)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No es válida la clave del distrito")
        consulta = consulta.join(Autoridad).filter(Autoridad.clave == autoridad_clave).filter(Autoridad.estatus == "A")
    if email is not None:
        try:
            email = safe_email(email, search_fragment=True)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No es válido el e-mail")
        consulta = consulta.filter(Usuario.email.contains(email))
    if nombres is not None:
        nombres = safe_string(nombres)
        if nombres != "":
            consulta = consulta.filter(Usuario.nombres.contains(nombres))
    return paginate(consulta.filter(Usuario.estatus == "A").order_by(Usuario.email))
