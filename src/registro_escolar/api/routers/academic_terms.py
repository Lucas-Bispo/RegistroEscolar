"""Rotas HTTP do contexto de periodos letivos."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from registro_escolar.dependencies import get_academic_term_service
from registro_escolar.schemas.academic_terms import (
    AcademicTermCreate,
    AcademicTermResponse,
)
from registro_escolar.services.academic_terms import (
    AcademicTermAlreadyExistsError,
    AcademicTermNotFoundError,
    AcademicTermService,
    InvalidAcademicTermRangeError,
)

router = APIRouter(prefix="/academic-terms", tags=["academic_terms"])


@router.get(
    "",
    response_model=list[AcademicTermResponse],
    summary="Lista periodos letivos",
)
def list_academic_terms(
    service: Annotated[AcademicTermService, Depends(get_academic_term_service)],
) -> list[AcademicTermResponse]:
    """Lista os periodos letivos atualmente cadastrados."""

    return [
        AcademicTermResponse.model_validate(term) for term in service.list_terms()
    ]


@router.get(
    "/{term_id}",
    response_model=AcademicTermResponse,
    summary="Busca um periodo letivo por identificador",
)
def get_academic_term(
    term_id: str,
    service: Annotated[AcademicTermService, Depends(get_academic_term_service)],
) -> AcademicTermResponse:
    """Retorna um periodo letivo especifico ou erro 404."""

    try:
        academic_term = service.get_term(term_id)
    except AcademicTermNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    return AcademicTermResponse.model_validate(academic_term)


@router.post(
    "",
    response_model=AcademicTermResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cria um novo periodo letivo",
)
def create_academic_term(
    payload: AcademicTermCreate,
    service: Annotated[AcademicTermService, Depends(get_academic_term_service)],
) -> AcademicTermResponse:
    """Cria um novo periodo letivo com validacao basica de negocio."""

    try:
        academic_term = service.create_term(
            name=payload.name,
            start_date=payload.start_date,
            end_date=payload.end_date,
            is_active=payload.is_active,
        )
    except AcademicTermAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc
    except InvalidAcademicTermRangeError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc

    return AcademicTermResponse.model_validate(academic_term)
