"""Testes unitarios do servico de formularios."""

from datetime import date

import pytest

from registro_escolar.domain.academic_terms.entities import AcademicTerm
from registro_escolar.domain.forms.entities import FormField
from registro_escolar.domain.schools.entities import School
from registro_escolar.infrastructure.repositories.in_memory_academic_term_repository import (
    InMemoryAcademicTermRepository,
)
from registro_escolar.infrastructure.repositories.in_memory_enrollment_form_repository import (
    InMemoryEnrollmentFormRepository,
)
from registro_escolar.infrastructure.repositories.in_memory_school_repository import (
    InMemorySchoolRepository,
)
from registro_escolar.services.forms import (
    EnrollmentFormAlreadyExistsError,
    EnrollmentFormService,
    InvalidEnrollmentFormFieldsError,
    InvalidEnrollmentFormRelationError,
)


def build_service() -> tuple[
    EnrollmentFormService,
    School,
    AcademicTerm,
]:
    """Cria um servico de formularios pronto para testes."""

    school_repository = InMemorySchoolRepository()
    academic_term_repository = InMemoryAcademicTermRepository()
    form_repository = InMemoryEnrollmentFormRepository()

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

    service = EnrollmentFormService(
        form_repository=form_repository,
        school_repository=school_repository,
        academic_term_repository=academic_term_repository,
    )
    return service, school, academic_term


def test_create_form_with_sorted_fields() -> None:
    """Deve criar formulario ordenando os campos pela ordem configurada."""

    service, school, academic_term = build_service()

    enrollment_form = service.create_form(
        school_id=school.id,
        academic_term_id=academic_term.id,
        name="Formulario Principal",
        description="Formulario base da campanha",
        fields=[
            FormField(label="Turno", field_type="select", options=("Manha",), order=2),
            FormField(label="Nome do aluno", field_type="text", order=1),
        ],
        is_published=True,
    )

    assert enrollment_form.is_published is True
    assert [field.label for field in enrollment_form.fields] == [
        "Nome do aluno",
        "Turno",
    ]


def test_create_form_rejects_duplicate_name_in_same_scope() -> None:
    """Nao deve permitir dois formularios com o mesmo nome no mesmo escopo."""

    service, school, academic_term = build_service()

    service.create_form(
        school_id=school.id,
        academic_term_id=academic_term.id,
        name="Formulario Principal",
        description="Primeira versao",
        fields=[FormField(label="Nome", field_type="text", order=1)],
        is_published=False,
    )

    with pytest.raises(EnrollmentFormAlreadyExistsError):
        service.create_form(
            school_id=school.id,
            academic_term_id=academic_term.id,
            name="  formulario   principal ",
            description="Duplicado",
            fields=[FormField(label="Nome", field_type="text", order=1)],
            is_published=False,
        )


def test_create_form_rejects_invalid_relations() -> None:
    """Nao deve criar formulario sem escola e periodo existentes."""

    service, _, _ = build_service()

    with pytest.raises(InvalidEnrollmentFormRelationError):
        service.create_form(
            school_id="missing-school",
            academic_term_id="missing-term",
            name="Formulario Principal",
            description="Invalido",
            fields=[FormField(label="Nome", field_type="text", order=1)],
            is_published=False,
        )


def test_create_form_rejects_select_without_options() -> None:
    """Nao deve aceitar campo select sem opcoes configuradas."""

    service, school, academic_term = build_service()

    with pytest.raises(InvalidEnrollmentFormFieldsError):
        service.create_form(
            school_id=school.id,
            academic_term_id=academic_term.id,
            name="Formulario Principal",
            description="Invalido",
            fields=[FormField(label="Turno", field_type="select", order=1)],
            is_published=False,
        )
