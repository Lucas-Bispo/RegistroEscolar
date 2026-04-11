"""Rotas HTTP do contexto de inscricoes publicas."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from registro_escolar.dependencies import get_enrollment_service
from registro_escolar.schemas.enrollments import (
    EnrollmentResponse,
    PublicEnrollmentCreate,
)
from registro_escolar.services.enrollments import (
    EnrollmentService,
    EnrollmentSubmissionLimitReachedError,
    InvalidEnrollmentSubmissionError,
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
