"""Rotas HTTP do contexto de inscricoes publicas."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from registro_escolar.dependencies import get_enrollment_service
from registro_escolar.schemas.enrollments import (
    EnrollmentResponse,
    EnrollmentStatusUpdate,
    PublicEnrollmentCreate,
)
from registro_escolar.services.enrollments import (
    ClassCapacityExceededError,
    EnrollmentNotFoundError,
    EnrollmentService,
    EnrollmentSubmissionLimitReachedError,
    InvalidEnrollmentSubmissionError,
    InvalidEnrollmentStatusTransitionError,
)
from registro_escolar.services.public_links import (
    PublicEnrollmentLinkExpiredError,
    PublicEnrollmentLinkInactiveError,
    PublicEnrollmentLinkNotFoundError,
)

router = APIRouter(prefix="/enrollments", tags=["enrollments"])


@router.get(
    "",
    response_model=list[EnrollmentResponse],
    summary="Lista inscricoes publicas recebidas",
)
def list_enrollments(
    service: Annotated[
        EnrollmentService,
        Depends(get_enrollment_service),
    ],
) -> list[EnrollmentResponse]:
    """Lista as inscricoes atualmente registradas."""

    return [EnrollmentResponse.model_validate(item) for item in service.list_enrollments()]


@router.post(
    "",
    response_model=EnrollmentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registra uma inscricao publica",
)
def create_public_enrollment(
    payload: PublicEnrollmentCreate,
    service: Annotated[
        EnrollmentService,
        Depends(get_enrollment_service),
    ],
) -> EnrollmentResponse:
    """Registra uma inscricao a partir de um token publico."""

    try:
        enrollment = service.create_public_enrollment(
            token=payload.token,
            class_id=payload.class_id,
            answers={item.order: item.value for item in payload.answers},
        )
    except (
        PublicEnrollmentLinkNotFoundError,
        PublicEnrollmentLinkInactiveError,
        PublicEnrollmentLinkExpiredError,
    ) as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except EnrollmentSubmissionLimitReachedError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc
    except InvalidEnrollmentSubmissionError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc

    return EnrollmentResponse.model_validate(enrollment)


@router.post(
    "/{enrollment_id}/status",
    response_model=EnrollmentResponse,
    summary="Atualiza o status operacional de uma inscricao",
)
def update_enrollment_status(
    enrollment_id: str,
    payload: EnrollmentStatusUpdate,
    service: Annotated[
        EnrollmentService,
        Depends(get_enrollment_service),
    ],
) -> EnrollmentResponse:
    """Atualiza o status da inscricao respeitando regras de capacidade."""

    try:
        enrollment = service.update_status(
            enrollment_id=enrollment_id,
            new_status=payload.status,
        )
    except EnrollmentNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except ClassCapacityExceededError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc
    except (
        InvalidEnrollmentStatusTransitionError,
        InvalidEnrollmentSubmissionError,
    ) as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc

    return EnrollmentResponse.model_validate(enrollment)
