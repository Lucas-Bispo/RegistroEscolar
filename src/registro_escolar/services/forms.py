"""Servicos de aplicacao relacionados a formularios dinamicos."""

from collections.abc import Sequence

from registro_escolar.domain.academic_terms.repositories import AcademicTermRepository
from registro_escolar.domain.forms.entities import EnrollmentForm, FormField
from registro_escolar.domain.forms.repositories import EnrollmentFormRepository
from registro_escolar.domain.schools.repositories import SchoolRepository

ALLOWED_FIELD_TYPES = {"text", "date", "email", "phone", "select", "upload"}


class EnrollmentFormAlreadyExistsError(ValueError):
    """Erro levantado quando tentamos cadastrar um formulario duplicado."""


class EnrollmentFormNotFoundError(LookupError):
    """Erro levantado quando um formulario nao e encontrado."""


class InvalidEnrollmentFormRelationError(ValueError):
    """Erro levantado quando escola ou periodo nao existem."""


class InvalidEnrollmentFormFieldsError(ValueError):
    """Erro levantado quando os campos informados sao invalidos."""


class EnrollmentFormService:
    """Orquestra os casos de uso do contexto de formularios."""

    def __init__(
        self,
        form_repository: EnrollmentFormRepository,
        school_repository: SchoolRepository,
        academic_term_repository: AcademicTermRepository,
    ) -> None:
        self._form_repository = form_repository
        self._school_repository = school_repository
        self._academic_term_repository = academic_term_repository

    def list_forms(self) -> Sequence[EnrollmentForm]:
        """Lista todos os formularios cadastrados."""

        return self._form_repository.list_all()

    def get_form(self, form_id: str) -> EnrollmentForm:
        """Busca um formulario pelo identificador."""

        enrollment_form = self._form_repository.get_by_id(form_id)
        if enrollment_form is None:
            msg = "Formulario nao encontrado."
            raise EnrollmentFormNotFoundError(msg)
        return enrollment_form

    def create_form(
        self,
        school_id: str,
        academic_term_id: str,
        name: str,
        description: str,
        fields: Sequence[FormField],
        is_published: bool,
    ) -> EnrollmentForm:
        """Cria um novo formulario com validacoes basicas de negocio."""

        school = self._school_repository.get_by_id(school_id)
        academic_term = self._academic_term_repository.get_by_id(academic_term_id)
        if school is None or academic_term is None:
            msg = "O formulario precisa estar vinculado a uma escola e a um periodo valido."
            raise InvalidEnrollmentFormRelationError(msg)

        validated_fields = self._validate_fields(fields)

        normalized_name = self._normalize_name(name)
        existing_form = self._form_repository.get_by_scope(
            school_id=school_id,
            academic_term_id=academic_term_id,
            normalized_name=normalized_name,
        )
        if existing_form is not None:
            msg = "Ja existe um formulario com este nome nessa escola e periodo."
            raise EnrollmentFormAlreadyExistsError(msg)

        enrollment_form = EnrollmentForm(
            school_id=school_id,
            academic_term_id=academic_term_id,
            name=name.strip(),
            description=description.strip(),
            fields=validated_fields,
            is_published=is_published,
        )
        return self._form_repository.add(enrollment_form)

    def _validate_fields(self, fields: Sequence[FormField]) -> tuple[FormField, ...]:
        """Valida os campos configurados antes da persistencia."""

        if not fields:
            msg = "O formulario precisa ter pelo menos um campo."
            raise InvalidEnrollmentFormFieldsError(msg)

        normalized_fields: list[FormField] = []
        seen_orders: set[int] = set()

        for field in fields:
            if field.field_type not in ALLOWED_FIELD_TYPES:
                msg = f"Tipo de campo invalido: {field.field_type}."
                raise InvalidEnrollmentFormFieldsError(msg)
            if field.order in seen_orders:
                msg = "A ordem dos campos deve ser unica dentro do formulario."
                raise InvalidEnrollmentFormFieldsError(msg)
            if field.field_type == "select" and not field.options:
                msg = "Campos do tipo select precisam ter opcoes."
                raise InvalidEnrollmentFormFieldsError(msg)
            if field.field_type != "select" and field.options:
                msg = "Apenas campos do tipo select podem ter opcoes."
                raise InvalidEnrollmentFormFieldsError(msg)

            seen_orders.add(field.order)
            normalized_fields.append(
                FormField(
                    label=field.label.strip(),
                    field_type=field.field_type.strip(),
                    required=field.required,
                    placeholder=field.placeholder.strip(),
                    options=tuple(option.strip() for option in field.options if option.strip()),
                    order=field.order,
                )
            )

        return tuple(sorted(normalized_fields, key=lambda item: item.order))

    @staticmethod
    def _normalize_name(value: str) -> str:
        """Normaliza o nome para comparacoes simples de unicidade."""

        return " ".join(value.lower().split())

