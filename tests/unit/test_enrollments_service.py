"""Testes unitarios do servico de inscricoes publicas."""

from datetime import date, datetime, timedelta, timezone

import pytest

from registro_escolar.domain.academic_terms.entities import AcademicTerm
from registro_escolar.domain.classes.entities import SchoolClass
from registro_escolar.domain.forms.entities import EnrollmentForm, FormField
from registro_escolar.domain.public_links.entities import PublicEnrollmentLink
from registro_escolar.domain.schools.entities import School
from registro_escolar.infrastructure.repositories.in_memory_academic_term_repository import (
    InMemoryAcademicTermRepository,
)
from registro_escolar.infrastructure.repositories.in_memory_enrollment_form_repository import (
    InMemoryEnrollmentFormRepository,
)
from registro_escolar.infrastructure.repositories.in_memory_enrollment_repository import (
    InMemoryEnrollmentRepository,
)
from registro_escolar.infrastructure.repositories.in_memory_public_enrollment_link_repository import (
    InMemoryPublicEnrollmentLinkRepository,
)
from registro_escolar.infrastructure.repositories.in_memory_school_class_repository import (
    InMemorySchoolClassRepository,
)
from registro_escolar.infrastructure.repositories.in_memory_school_repository import (
    InMemorySchoolRepository,
)
from registro_escolar.services.enrollments import (
    ClassCapacityExceededError,
    EnrollmentService,
    InvalidEnrollmentStatusTransitionError,
    EnrollmentSubmissionLimitReachedError,
    InvalidEnrollmentSubmissionError,
)


def build_service() -> tuple[
    EnrollmentService,
    PublicEnrollmentLink,
    SchoolClass,
]:
    """Cria um servico de inscricoes pronto para testes."""

    school_repository = InMemorySchoolRepository()
    academic_term_repository = InMemoryAcademicTermRepository()
    class_repository = InMemorySchoolClassRepository()
    form_repository = InMemoryEnrollmentFormRepository()
    link_repository = InMemoryPublicEnrollmentLinkRepository()
    enrollment_repository = InMemoryEnrollmentRepository()

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
    school_class = class_repository.add(
        SchoolClass(
            school_id=school.id,
            academic_term_id=academic_term.id,
            name="1A",
            shift="Manha",
            capacity=30,
            is_active=True,
        )
    )
    enrollment_form = form_repository.add(
        EnrollmentForm(
            school_id=school.id,
            academic_term_id=academic_term.id,
            name="Formulario Publicado",
            description="Base da campanha",
            fields=(
                FormField(label="Nome do aluno", field_type="text", order=1),
                FormField(label="Email", field_type="email", order=2),
                FormField(
                    label="Turno",
                    field_type="select",
                    options=("Manha", "Tarde"),
                    order=3,
                ),
            ),
            is_published=True,
        )
    )
    public_link = link_repository.add(
        PublicEnrollmentLink(
            school_id=school.id,
            academic_term_id=academic_term.id,
            form_id=enrollment_form.id,
            token="token-publico-valido-123456",
            expires_at=datetime.now(timezone.utc) + timedelta(days=10),
            max_submissions=2,
            is_active=True,
        )
    )

    service = EnrollmentService(
        enrollment_repository=enrollment_repository,
        public_link_repository=link_repository,
        school_repository=school_repository,
        academic_term_repository=academic_term_repository,
        class_repository=class_repository,
        form_repository=form_repository,
    )
    return service, public_link, school_class


def test_create_public_enrollment_generates_protocol() -> None:
    """Deve registrar uma inscricao publica com protocolo."""

    service, public_link, school_class = build_service()

    enrollment = service.create_public_enrollment(
        token=public_link.token,
        class_id=school_class.id,
        answers={
            1: "Ana Souza",
            2: "ana@example.com",
            3: "Manha",
        },
    )

    assert enrollment.protocol.startswith("MAT-")
    assert enrollment.status == "submitted"
    assert len(enrollment.answers) == 3


def test_create_public_enrollment_rejects_missing_required_field() -> None:
    """Nao deve aceitar submissao sem todos os campos obrigatorios."""

    service, public_link, school_class = build_service()

    with pytest.raises(InvalidEnrollmentSubmissionError):
        service.create_public_enrollment(
            token=public_link.token,
            class_id=school_class.id,
            answers={
                1: "Ana Souza",
                3: "Manha",
            },
        )


def test_create_public_enrollment_rejects_invalid_select_option() -> None:
    """Nao deve aceitar opcao fora do conjunto publicado."""

    service, public_link, school_class = build_service()

    with pytest.raises(InvalidEnrollmentSubmissionError):
        service.create_public_enrollment(
            token=public_link.token,
            class_id=school_class.id,
            answers={
                1: "Ana Souza",
                2: "ana@example.com",
                3: "Noite",
            },
        )


def test_create_public_enrollment_respects_submission_limit() -> None:
    """Nao deve exceder o limite configurado no link publico."""

    service, public_link, school_class = build_service()

    for name in ("Ana Souza", "Bia Lima"):
        service.create_public_enrollment(
            token=public_link.token,
            class_id=school_class.id,
            answers={
                1: name,
                2: "responsavel@example.com",
                3: "Manha",
            },
        )

    with pytest.raises(EnrollmentSubmissionLimitReachedError):
        service.create_public_enrollment(
            token=public_link.token,
            class_id=school_class.id,
            answers={
                1: "Carla Rocha",
                2: "carla@example.com",
                3: "Manha",
            },
        )


def test_update_status_confirms_enrollment_with_available_capacity() -> None:
    """Deve confirmar inscricao quando ainda houver vaga na turma."""

    service, public_link, school_class = build_service()
    enrollment = service.create_public_enrollment(
        token=public_link.token,
        class_id=school_class.id,
        answers={
            1: "Ana Souza",
            2: "ana@example.com",
            3: "Manha",
        },
    )

    updated_enrollment = service.update_status(
        enrollment_id=enrollment.id,
        new_status="confirmed",
    )

    assert updated_enrollment.status == "confirmed"
    assert service.count_confirmed_enrollments(school_class.id) == 1


def test_update_status_rejects_confirmation_when_class_is_full() -> None:
    """Nao deve confirmar quando a turma ja ocupou toda a capacidade."""

    service, public_link, school_class = build_service()
    school_class.capacity = 1

    first_enrollment = service.create_public_enrollment(
        token=public_link.token,
        class_id=school_class.id,
        answers={
            1: "Ana Souza",
            2: "ana@example.com",
            3: "Manha",
        },
    )
    second_enrollment = service.create_public_enrollment(
        token=public_link.token,
        class_id=school_class.id,
        answers={
            1: "Bia Lima",
            2: "bia@example.com",
            3: "Manha",
        },
    )

    service.update_status(first_enrollment.id, "confirmed")

    with pytest.raises(ClassCapacityExceededError):
        service.update_status(second_enrollment.id, "confirmed")


def test_update_status_rejects_invalid_transition_from_confirmed() -> None:
    """Nao deve permitir reabrir inscricao ja confirmada neste recorte."""

    service, public_link, school_class = build_service()
    enrollment = service.create_public_enrollment(
        token=public_link.token,
        class_id=school_class.id,
        answers={
            1: "Ana Souza",
            2: "ana@example.com",
            3: "Manha",
        },
    )

    service.update_status(enrollment.id, "confirmed")

    with pytest.raises(InvalidEnrollmentStatusTransitionError):
        service.update_status(enrollment.id, "rejected")
