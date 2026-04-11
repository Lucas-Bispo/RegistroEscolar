"""Rotas HTTP do contexto de formularios dinamicos."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from registro_escolar.dependencies import get_enrollment_form_service
from registro_escolar.domain.forms.entities import FormField
from registro_escolar.schemas.forms import (
    EnrollmentFormCreate,
    EnrollmentFormResponse,
)
from registro_escolar.services.forms import (
    EnrollmentFormAlreadyExistsError,
    EnrollmentFormNotFoundError,
    EnrollmentFormService,
    InvalidEnrollmentFormFieldsError,
    InvalidEnrollmentFormRelationError,
)

router = APIRouter(prefix="/forms", tags=["forms"])


@router.get(
    "",
    response_model=list[EnrollmentFormResponse],
    summary="Lista formularios dinamicos",
)
def list_forms(
    service: Annotated[
        EnrollmentFormService,
        Depends(get_enrollment_form_service),
    ],
) -> list[EnrollmentFormResponse]:
    """Lista os formularios atualmente cadastrados."""

    return [EnrollmentFormResponse.model_validate(item) for item in service.list_forms()]


@router.get(
    "/{form_id}",
    response_model=EnrollmentFormResponse,
    summary="Busca um formulario por identificador",
)
def get_form(
    form_id: str,
    service: Annotated[
        EnrollmentFormService,
        Depends(get_enrollment_form_service),
    ],
) -> EnrollmentFormResponse:
    """Retorna um formulario especifico ou erro 404."""

    try:
        enrollment_form = service.get_form(form_id)
    except EnrollmentFormNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    return EnrollmentFormResponse.model_validate(enrollment_form)


@router.post(
    "",
    response_model=EnrollmentFormResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cria um novo formulario dinamico",
)
def create_form(
    payload: EnrollmentFormCreate,
    service: Annotated[
        EnrollmentFormService,
        Depends(get_enrollment_form_service),
    ],
) -> EnrollmentFormResponse:
    """Cria um novo formulario com validacoes basicas de negocio."""

    try:
        enrollment_form = service.create_form(
            school_id=payload.school_id,
            academic_term_id=payload.academic_term_id,
            name=payload.name,
            description=payload.description,
            fields=[
                FormField(
                    label=field.label,
                    field_type=field.field_type,
                    required=field.required,
                    placeholder=field.placeholder,
                    options=tuple(field.options),
                    order=field.order,
                )
                for field in payload.fields
            ],
            is_published=payload.is_published,
        )
    except EnrollmentFormAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc
    except (
        InvalidEnrollmentFormFieldsError,
        InvalidEnrollmentFormRelationError,
    ) as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc

    return EnrollmentFormResponse.model_validate(enrollment_form)

