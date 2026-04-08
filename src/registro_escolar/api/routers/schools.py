"""Rotas HTTP do contexto de escolas."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from registro_escolar.dependencies import get_school_service
from registro_escolar.schemas.schools import SchoolCreate, SchoolResponse
from registro_escolar.services.schools import (
    SchoolAlreadyExistsError,
    SchoolNotFoundError,
    SchoolService,
)

router = APIRouter(prefix="/schools", tags=["schools"])


@router.get("", response_model=list[SchoolResponse], summary="Lista escolas")
def list_schools(
    service: Annotated[SchoolService, Depends(get_school_service)],
) -> list[SchoolResponse]:
    """Lista as escolas atualmente disponiveis."""

    return [SchoolResponse.model_validate(school) for school in service.list_schools()]


@router.get(
    "/{school_id}",
    response_model=SchoolResponse,
    summary="Busca uma escola por identificador",
)
def get_school(
    school_id: str,
    service: Annotated[SchoolService, Depends(get_school_service)],
) -> SchoolResponse:
    """Retorna uma escola especifica ou erro 404."""

    try:
        school = service.get_school(school_id)
    except SchoolNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    return SchoolResponse.model_validate(school)


@router.post(
    "",
    response_model=SchoolResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cria uma nova escola",
)
def create_school(
    payload: SchoolCreate,
    service: Annotated[SchoolService, Depends(get_school_service)],
) -> SchoolResponse:
    """Cria uma nova escola com validacao basica de negocio."""

    try:
        school = service.create_school(
            name=payload.name,
            city=payload.city,
            state=payload.state,
        )
    except SchoolAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

    return SchoolResponse.model_validate(school)
