"""Servicos de aplicacao relacionados a inscricoes publicas."""

from collections.abc import Mapping, Sequence
from datetime import date, datetime, timezone
from re import fullmatch
from secrets import randbelow

from registro_escolar.domain.academic_terms.repositories import AcademicTermRepository
from registro_escolar.domain.classes.repositories import SchoolClassRepository
from registro_escolar.domain.enrollments.entities import Enrollment, EnrollmentAnswer
from registro_escolar.domain.enrollments.repositories import EnrollmentRepository
from registro_escolar.domain.forms.entities import EnrollmentForm, FormField
from registro_escolar.domain.forms.repositories import EnrollmentFormRepository
from registro_escolar.domain.public_links.entities import PublicEnrollmentLink
from registro_escolar.domain.public_links.repositories import (
    PublicEnrollmentLinkRepository,
)
from registro_escolar.domain.schools.repositories import SchoolRepository
from registro_escolar.services.public_links import (
    PublicEnrollmentLinkExpiredError,
    PublicEnrollmentLinkInactiveError,
    PublicEnrollmentLinkNotFoundError,
)


class InvalidEnrollmentSubmissionError(ValueError):
    """Erro levantado quando a inscricao publica e invalida."""


class EnrollmentSubmissionLimitReachedError(ValueError):
    """Erro levantado quando o link atingiu o limite configurado."""


class EnrollmentService:
    """Orquestra os casos de uso do contexto de inscricoes."""

    def __init__(
        self,
        enrollment_repository: EnrollmentRepository,
        public_link_repository: PublicEnrollmentLinkRepository,
        school_repository: SchoolRepository,
        academic_term_repository: AcademicTermRepository,
        class_repository: SchoolClassRepository,
        form_repository: EnrollmentFormRepository,
    ) -> None:
        self._enrollment_repository = enrollment_repository
        self._public_link_repository = public_link_repository
        self._school_repository = school_repository
        self._academic_term_repository = academic_term_repository
        self._class_repository = class_repository
        self._form_repository = form_repository

    def list_enrollments(self) -> Sequence[Enrollment]:
        """Lista todas as inscricoes registradas."""

        return self._enrollment_repository.list_all()

    def create_public_enrollment(
        self,
        token: str,
        class_id: str,
        answers: Mapping[int, str],
    ) -> Enrollment:
        """Registra uma inscricao publica validando o formulario publicado."""

        public_link = self._resolve_active_link(token)
        school = self._school_repository.get_by_id(public_link.school_id)
        academic_term = self._academic_term_repository.get_by_id(
            public_link.academic_term_id
        )
        school_class = self._class_repository.get_by_id(class_id)
        enrollment_form = self._form_repository.get_by_id(public_link.form_id)

        if (
            school is None
            or academic_term is None
            or school_class is None
            or enrollment_form is None
        ):
            msg = "A inscricao precisa apontar para escola, periodo, turma e formulario validos."
            raise InvalidEnrollmentSubmissionError(msg)
        if school_class.school_id != public_link.school_id:
            msg = "A turma selecionada nao pertence a escola do link publico."
            raise InvalidEnrollmentSubmissionError(msg)
        if school_class.academic_term_id != public_link.academic_term_id:
            msg = "A turma selecionada nao pertence ao periodo letivo do link publico."
            raise InvalidEnrollmentSubmissionError(msg)
        if not school_class.is_active:
            msg = "A turma selecionada esta inativa no momento."
            raise InvalidEnrollmentSubmissionError(msg)
        if not enrollment_form.is_published:
            msg = "O formulario vinculado ao link publico precisa estar publicado."
            raise InvalidEnrollmentSubmissionError(msg)

        current_count = self._enrollment_repository.count_by_public_link_id(
            public_link.id
        )
        if current_count >= public_link.max_submissions:
            msg = "Este link publico ja atingiu o limite configurado de inscricoes."
            raise EnrollmentSubmissionLimitReachedError(msg)

        validated_answers = self._validate_answers(
            enrollment_form=enrollment_form,
            answers=self._normalize_answers(answers),
        )

        enrollment = Enrollment(
            school_id=public_link.school_id,
            academic_term_id=public_link.academic_term_id,
            class_id=school_class.id,
            form_id=enrollment_form.id,
            public_link_id=public_link.id,
            protocol=self._generate_protocol(),
            answers=validated_answers,
        )
        return self._enrollment_repository.add(enrollment)

    def _resolve_active_link(self, token: str) -> PublicEnrollmentLink:
        """Resolve um token publico ja validando disponibilidade do link."""

        public_link = self._public_link_repository.get_by_token(token)
        if public_link is None:
            msg = "Link publico nao encontrado."
            raise PublicEnrollmentLinkNotFoundError(msg)
        if not public_link.is_active:
            msg = "Link publico inativo."
            raise PublicEnrollmentLinkInactiveError(msg)
        if public_link.expires_at <= datetime.now(timezone.utc):
            msg = "Link publico expirado."
            raise PublicEnrollmentLinkExpiredError(msg)
        return public_link

    def _validate_answers(
        self,
        enrollment_form: EnrollmentForm,
        answers: Mapping[int, str],
    ) -> tuple[EnrollmentAnswer, ...]:
        """Valida e normaliza as respostas conforme o formulario publicado."""

        allowed_orders = {field.order for field in enrollment_form.fields}
        if set(answers).difference(allowed_orders):
            msg = "Foram enviados campos que nao pertencem ao formulario publicado."
            raise InvalidEnrollmentSubmissionError(msg)

        normalized_answers: list[EnrollmentAnswer] = []
        for field in enrollment_form.fields:
            value = answers.get(field.order, "")
            if field.required and not value:
                msg = f"O campo '{field.label}' e obrigatorio."
                raise InvalidEnrollmentSubmissionError(msg)
            if value:
                self._validate_field_value(field=field, value=value)
            normalized_answers.append(
                EnrollmentAnswer(
                    field_order=field.order,
                    field_label=field.label,
                    value=value,
                )
            )

        return tuple(normalized_answers)

    def _validate_field_value(self, field: FormField, value: str) -> None:
        """Aplica validacoes simples por tipo de campo."""

        if field.field_type == "select" and value not in field.options:
            msg = f"O campo '{field.label}' precisa receber uma opcao valida."
            raise InvalidEnrollmentSubmissionError(msg)
        if field.field_type == "date":
            try:
                date.fromisoformat(value)
            except ValueError as exc:
                msg = f"O campo '{field.label}' precisa informar uma data valida."
                raise InvalidEnrollmentSubmissionError(msg) from exc
        if field.field_type == "email" and not fullmatch(
            r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
            value,
        ):
            msg = f"O campo '{field.label}' precisa informar um email valido."
            raise InvalidEnrollmentSubmissionError(msg)
        if field.field_type == "phone":
            digits = "".join(char for char in value if char.isdigit())
            if len(digits) < 10:
                msg = f"O campo '{field.label}' precisa informar um telefone valido."
                raise InvalidEnrollmentSubmissionError(msg)

    @staticmethod
    def _normalize_answers(answers: Mapping[int, str]) -> dict[int, str]:
        """Remove espacos e garante um formato uniforme das respostas."""

        return {order: value.strip() for order, value in answers.items()}

    @staticmethod
    def _generate_protocol() -> str:
        """Gera um protocolo simples e amigavel para o responsavel."""

        now = datetime.now(timezone.utc)
        return f"MAT-{now:%Y%m%d}-{randbelow(1_000_000):06d}"
