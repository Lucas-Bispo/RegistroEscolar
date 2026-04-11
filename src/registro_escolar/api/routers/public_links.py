"""Rotas HTTP do contexto de links publicos."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from registro_escolar.dependencies import get_public_enrollment_link_service
from registro_escolar.schemas.public_links import (
    PublicEnrollmentLinkCreate,
    PublicEnrollmentLinkResponse,
)
from registro_escolar.services.public_links import (
    InvalidPublicEnrollmentLinkConfigurationError,
    InvalidPublicEnrollmentLinkRelationError,
    PublicEnrollmentLinkNotFoundError,
    PublicEnrollmentLinkService,
)

router = APIRouter(prefix="/public-links", tags=["public-links"])


@router.get(
    "",
    response_model=list[PublicEnrollmentLinkResponse],
    summary="Lista links publicos",
)
def list_public_links(
    service: Annotated[
        PublicEnrollmentLinkService,
        Depends(get_public_enrollment_link_service),
    ],
) -> list[PublicEnrollmentLinkResponse]:
    """Lista os links publicos atualmente cadastrados."""

    return [
        PublicEnrollmentLinkResponse.model_validate(item)
        for item in service.list_links()
    ]


@router.get(
    "/{link_id}",
    response_model=PublicEnrollmentLinkResponse,
    summary="Busca um link publico por identificador",
)
def get_public_link(
    link_id: str,
    service: Annotated[
        PublicEnrollmentLinkService,
        Depends(get_public_enrollment_link_service),
    ],
) -> PublicEnrollmentLinkResponse:
    """Retorna um link publico especifico ou erro 404."""

    try:
        public_link = service.get_link(link_id)
    except PublicEnrollmentLinkNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    return PublicEnrollmentLinkResponse.model_validate(public_link)


@router.post(
    "",
    response_model=PublicEnrollmentLinkResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cria um novo link publico",
)
def create_public_link(
    payload: PublicEnrollmentLinkCreate,
    service: Annotated[
        PublicEnrollmentLinkService,
        Depends(get_public_enrollment_link_service),
    ],
) -> PublicEnrollmentLinkResponse:
    """Cria um novo link publico para um formulario publicado."""

    try:
        public_link = service.create_link(
            school_id=payload.school_id,
            academic_term_id=payload.academic_term_id,
            form_id=payload.form_id,
            expires_at=payload.expires_at,
            max_submissions=payload.max_submissions,
            is_active=payload.is_active,
        )
    except (
        InvalidPublicEnrollmentLinkRelationError,
        InvalidPublicEnrollmentLinkConfigurationError,
    ) as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc

    return PublicEnrollmentLinkResponse.model_validate(public_link)
