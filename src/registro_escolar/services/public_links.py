"""Servicos de aplicacao relacionados a links publicos."""

from collections.abc import Sequence
from datetime import datetime, timezone
from secrets import token_urlsafe

from registro_escolar.domain.academic_terms.repositories import AcademicTermRepository
from registro_escolar.domain.forms.repositories import EnrollmentFormRepository
from registro_escolar.domain.public_links.entities import PublicEnrollmentLink
from registro_escolar.domain.public_links.repositories import (
    PublicEnrollmentLinkRepository,
)
from registro_escolar.domain.schools.repositories import SchoolRepository


class PublicEnrollmentLinkNotFoundError(LookupError):
    """Erro levantado quando um link publico nao e encontrado."""


class PublicEnrollmentLinkInactiveError(ValueError):
    """Erro levantado quando o link publico esta inativo."""


class PublicEnrollmentLinkExpiredError(ValueError):
    """Erro levantado quando o link publico expirou."""


class InvalidPublicEnrollmentLinkRelationError(ValueError):
    """Erro levantado quando o formulario nao combina com o escopo informado."""


class InvalidPublicEnrollmentLinkConfigurationError(ValueError):
    """Erro levantado quando a configuracao do link publico e invalida."""


class PublicEnrollmentLinkService:
    """Orquestra os casos de uso do contexto de links publicos."""

    def __init__(
        self,
        link_repository: PublicEnrollmentLinkRepository,
        school_repository: SchoolRepository,
        academic_term_repository: AcademicTermRepository,
        form_repository: EnrollmentFormRepository,
    ) -> None:
        self._link_repository = link_repository
        self._school_repository = school_repository
        self._academic_term_repository = academic_term_repository
        self._form_repository = form_repository

    def list_links(self) -> Sequence[PublicEnrollmentLink]:
        """Lista todos os links publicos cadastrados."""

        return self._link_repository.list_all()

    def get_link(self, link_id: str) -> PublicEnrollmentLink:
        """Busca um link publico pelo identificador."""

        public_link = self._link_repository.get_by_id(link_id)
        if public_link is None:
            msg = "Link publico nao encontrado."
            raise PublicEnrollmentLinkNotFoundError(msg)
        return public_link

    def create_link(
        self,
        school_id: str,
        academic_term_id: str,
        form_id: str,
        expires_at: datetime,
        max_submissions: int,
        is_active: bool,
    ) -> PublicEnrollmentLink:
        """Cria um novo link publico validando o escopo publicado."""

        school = self._school_repository.get_by_id(school_id)
        academic_term = self._academic_term_repository.get_by_id(academic_term_id)
        enrollment_form = self._form_repository.get_by_id(form_id)

        if school is None or academic_term is None or enrollment_form is None:
            msg = "Link publico precisa apontar para escola, periodo e formulario validos."
            raise InvalidPublicEnrollmentLinkRelationError(msg)
        if enrollment_form.school_id != school_id:
            msg = "O formulario precisa pertencer a escola selecionada."
            raise InvalidPublicEnrollmentLinkRelationError(msg)
        if enrollment_form.academic_term_id != academic_term_id:
            msg = "O formulario precisa pertencer ao periodo letivo selecionado."
            raise InvalidPublicEnrollmentLinkRelationError(msg)
        if not enrollment_form.is_published:
            msg = "Somente formularios publicados podem gerar link publico."
            raise InvalidPublicEnrollmentLinkRelationError(msg)
        if max_submissions <= 0:
            msg = "O limite de submisses deve ser maior que zero."
            raise InvalidPublicEnrollmentLinkConfigurationError(msg)

        now = datetime.now(timezone.utc)
        normalized_expires_at = self._ensure_utc(expires_at)
        if normalized_expires_at <= now:
            msg = "A expiracao do link publico precisa estar no futuro."
            raise InvalidPublicEnrollmentLinkConfigurationError(msg)

        public_link = PublicEnrollmentLink(
            school_id=school_id,
            academic_term_id=academic_term_id,
            form_id=form_id,
            token=token_urlsafe(24),
            expires_at=normalized_expires_at,
            max_submissions=max_submissions,
            is_active=is_active,
        )
        return self._link_repository.add(public_link)

    def resolve_active_link(self, token: str) -> PublicEnrollmentLink:
        """Resolve um token publico ja validando disponibilidade do link."""

        public_link = self._link_repository.get_by_token(token)
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

    @staticmethod
    def _ensure_utc(value: datetime) -> datetime:
        """Garante um datetime timezone-aware em UTC."""

        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)

