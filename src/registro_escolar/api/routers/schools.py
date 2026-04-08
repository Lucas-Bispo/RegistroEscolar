"""Rotas HTTP do contexto de escolas."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from registro_escolar.domain.schools.repositories import SchoolRepository
from registro_escolar.infrastructure.repositories.in_memory_school_repository import (
    InMemorySchoolRepository,
)
from registro_escolar.schemas.schools import SchoolCreate, SchoolResponse
from registro_escolar.services.schools import (
    SchoolAlreadyExistsError,
    SchoolNotFoundError,
    SchoolService,
)

router = APIRouter(prefix="/schools", tags=["schools"])

_school_repository = InMemorySchoolRepository()


def get_school_repository() -> SchoolRepository:
    """Fornece a implementacao concreta do repositorio.

    Mantemos esta funcao separada para facilitar a futura troca por
    um repositorio com banco de dados e tambem para simplificar testes.
    """

    return _school_repository


def get_school_service(
    repository: Annotated[SchoolRepository, Depends(get_school_repository)],
) -> SchoolService:
    """Constroi o servico de escolas a partir do repositorio."""

    return SchoolService(repository=repository)


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
