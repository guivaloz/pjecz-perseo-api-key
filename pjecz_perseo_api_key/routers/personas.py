"""
Personas
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.exc import MultipleResultsFound, NoResultFound

from pjecz_perseo_api_key.dependencies.authentications import UsuarioInDB, get_current_active_user
from pjecz_perseo_api_key.dependencies.database import Session, get_db
from pjecz_perseo_api_key.dependencies.fastapi_pagination_custom_page import CustomPage
from pjecz_perseo_api_key.dependencies.safe_string import safe_curp, safe_rfc, safe_string
from pjecz_perseo_api_key.models.permisos import Permiso
from pjecz_perseo_api_key.models.personas import Persona
from pjecz_perseo_api_key.models.tabuladores import Tabulador
from pjecz_perseo_api_key.schemas.personas import OnePersonaOut, PersonaOut

personas = APIRouter(prefix="/api/v5/personas", tags=["personas"])


@personas.get("/{rfc}", response_model=OnePersonaOut)
async def detalle_persona(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    rfc: str,
):
    """Detalle de una persona a partir de su RFC"""
    if current_user.permissions.get("PERSONAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        rfc = safe_rfc(rfc)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No es válido el RFC")
    try:
        usuario = database.query(Persona).filter_by(rfc=rfc).one()
    except MultipleResultsFound, NoResultFound:
        return OnePersonaOut(success=False, message="No existe ese usuario")
    if usuario.estatus != "A":
        return OnePersonaOut(success=False, message="No está habilitado ese usuario")
    return OnePersonaOut(success=True, message=f"Detalle de {rfc}", data=PersonaOut.model_validate(usuario))


@personas.get("", response_model=CustomPage[PersonaOut])
async def paginado_personas(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    apellido_primero: str | None = None,
    apellido_segundo: str | None = None,
    curp: str | None = None,
    nombres: str | None = None,
    rfc: str | None = None,
    tabulador_id: int | None = None,
):
    """Paginado de personas"""
    if current_user.permissions.get("PERSONAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    consulta = database.query(Persona)
    if apellido_primero is not None:
        apellido_primero = safe_string(apellido_primero, save_enie=True)
        if apellido_primero != "":
            consulta = consulta.filter(Persona.apellido_primero.contains(apellido_primero))
    if apellido_segundo is not None:
        apellido_segundo = safe_string(apellido_segundo, save_enie=True)
        if apellido_segundo != "":
            consulta = consulta.filter(Persona.apellido_segundo.contains(apellido_segundo))
    if nombres is not None:
        nombres = safe_string(nombres, save_enie=True)
        if nombres != "":
            consulta = consulta.filter(Persona.nombres.contains(nombres))
    if curp is not None:
        try:
            curp = safe_curp(curp, search_fragment=True)
        except ValueError as error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No es válido el CURP")
        consulta = consulta.filter(Persona.curp.contains(curp))
    elif rfc is not None:
        try:
            rfc = safe_rfc(rfc)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No es válido el RFC")
        consulta = consulta.filter(Persona.rfc.contains(rfc))
    if tabulador_id is not None:
        consulta = consulta.join(Tabulador).filter(Tabulador.id == tabulador_id).filter(Tabulador.estatus == "A")
    return paginate(consulta.filter(Persona.estatus == "A").order_by(Persona.rfc))
