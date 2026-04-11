"""Testes unitarios do servico de links publicos."""

from datetime import date, datetime, timedelta, timezone

import pytest

from registro_escolar.domain.academic_terms.entities import AcademicTerm
from registro_escolar.domain.forms.entities import EnrollmentForm, FormField
from registro_escolar.domain.schools.entities import School
from registro_escolar.infrastructure.repositories.in_memory_academic_term_repository import (
    InMemoryAcademicTermRepository,
)
from registro_escolar.infrastructure.repositories.in_memory_enrollment_form_repository import (
    InMemoryEnrollmentFormRepository,
)
from registro_escolar.infrastructure.repositories.in_memory_public_enrollment_link_repository import (
    InMemoryPublicEnrollmentLinkRepository,
)
from registro_escolar.infrastructure.repositories.in_memory_school_repository import (
    InMemorySchoolRepository,
)
from registro_escolar.services.public_links import (
    InvalidPublicEnrollmentLinkConfigurationError,
    InvalidPublicEnrollmentLinkRelationError,
    PublicEnrollmentLinkExpiredError,
    PublicEnrollmentLinkService,
)


def build_service() -> tuple[
    PublicEnrollmentLinkService,
    School,
    AcademicTerm,
    EnrollmentForm,
]:
    """Cria um servico de links publicos pronto para testes."""

    school_repository = InMemorySchoolRepository()
    academic_term_repository = InMemoryAcademicTermRepository()
    form_repository = InMemoryEnrollmentFormRepository()
    link_repository = InMemoryPublicEnrollmentLinkRepository()

    school = school_repository.add(
        School(name="Colegio Horizonte", city="Sao Paulo", state="SP")
    )
    academic_term = academic_term_repository.add(
        AcademicTerm(
            name="Matricula 2028",
            start_date=date(2028, 1, 10),
            end_date=date(2028, 12, 20),
            is_active=True,
        )
    )
    enrollment_form = form_repository.add(
        EnrollmentForm(
            school_id=school.id,
            academic_term_id=academic_term.id,
            name="Formulario Publicado",
            description="Base da campanha",
            fields=(FormField(label="Nome", field_type="text", order=1),),
            is_published=True,
        )
    )

    service = PublicEnrollmentLinkService(
        link_repository=link_repository,
        school_repository=school_repository,
        academic_term_repository=academic_term_repository,
        form_repository=form_repository,
    )
    return service, school, academic_term, enrollment_form


def test_create_public_link_for_published_form() -> None:
    """Deve criar link publico com token para formulario publicado."""

    service, school, academic_term, enrollment_form = build_service()

    public_link = service.create_link(
        school_id=school.id,
        academic_term_id=academic_term.id,
        form_id=enrollment_form.id,
        expires_at=datetime.now(timezone.utc) + timedelta(days=10),
        max_submissions=500,
        is_active=True,
    )

    assert public_link.token
    assert public_link.form_id == enrollment_form.id


def test_create_public_link_rejects_unpublished_form() -> None:
    """Nao deve permitir link publico para formulario em rascunho."""

    service, school, academic_term, _ = build_service()
    draft_form = service._form_repository.add(
        EnrollmentForm(
            school_id=school.id,
            academic_term_id=academic_term.id,
            name="Formulario Rascunho",
            description="Ainda nao publicado",
            fields=(FormField(label="Nome", field_type="text", order=1),),
            is_published=False,
        )
    )

    with pytest.raises(InvalidPublicEnrollmentLinkRelationError):
        service.create_link(
            school_id=school.id,
            academic_term_id=academic_term.id,
            form_id=draft_form.id,
            expires_at=datetime.now(timezone.utc) + timedelta(days=10),
            max_submissions=500,
            is_active=True,
        )


def test_create_public_link_rejects_past_expiration() -> None:
    """Nao deve aceitar links com expiracao no passado."""

    service, school, academic_term, enrollment_form = build_service()

    with pytest.raises(InvalidPublicEnrollmentLinkConfigurationError):
        service.create_link(
            school_id=school.id,
            academic_term_id=academic_term.id,
            form_id=enrollment_form.id,
            expires_at=datetime.now(timezone.utc) - timedelta(minutes=1),
            max_submissions=100,
            is_active=True,
        )


def test_resolve_active_link_rejects_expired_link() -> None:
    """Nao deve resolver um link expirado."""

    service, school, academic_term, enrollment_form = build_service()
    expired_link = service.create_link(
        school_id=school.id,
        academic_term_id=academic_term.id,
        form_id=enrollment_form.id,
        expires_at=datetime.now(timezone.utc) + timedelta(days=1),
        max_submissions=100,
        is_active=True,
    )
    expired_link.expires_at = datetime.now(timezone.utc) - timedelta(minutes=1)

    with pytest.raises(PublicEnrollmentLinkExpiredError):
        service.resolve_active_link(expired_link.token)
