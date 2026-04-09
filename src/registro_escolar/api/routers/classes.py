"""Rotas HTTP do contexto de turmas."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from registro_escolar.dependencies import get_school_class_service
from registro_escolar.schemas.classes import SchoolClassCreate, SchoolClassResponse
from registro_escolar.services.classes import (
    InvalidClassCapacityError,
    InvalidClassRelationError,
    SchoolClassAlreadyExistsError,
    SchoolClassNotFoundError,
    SchoolClassService,
)

router = APIRouter(prefix="/classes", tags=["classes"])


@router.get("", response_model=list[SchoolClassResponse], summary="Lista turmas")
def list_classes(
    service: Annotated[SchoolClassService, Depends(get_school_class_service)],
) -> list[SchoolClassResponse]:
    """Lista as turmas atualmente cadastradas."""

    return [SchoolClassResponse.model_validate(item) for item in service.list_classes()]


@router.get(
    "/{class_id}",
    response_model=SchoolClassResponse,
    summary="Busca uma turma por identificador",
)
def get_class(
    class_id: str,
    service: Annotated[SchoolClassService, Depends(get_school_class_service)],
) -> SchoolClassResponse:
    """Retorna uma turma especifica ou erro 404."""

    try:
        school_class = service.get_class(class_id)
    except SchoolClassNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    return SchoolClassResponse.model_validate(school_class)


@router.post(
    "",
    response_model=SchoolClassResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cria uma nova turma",
)
def create_class(
    payload: SchoolClassCreate,
    service: Annotated[SchoolClassService, Depends(get_school_class_service)],
) -> SchoolClassResponse:
    """Cria uma nova turma com validacoes basicas de negocio."""

    try:
        school_class = service.create_class(
            school_id=payload.school_id,
            academic_term_id=payload.academic_term_id,
            name=payload.name,
            shift=payload.shift,
            capacity=payload.capacity,
            is_active=payload.is_active,
        )
    except SchoolClassAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc
    except (InvalidClassCapacityError, InvalidClassRelationError) as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc

    return SchoolClassResponse.model_validate(school_class)
