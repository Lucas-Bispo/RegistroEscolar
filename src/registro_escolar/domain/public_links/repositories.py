"""Contratos de persistencia para o contexto de links publicos."""

from collections.abc import Sequence
from typing import Protocol

from registro_escolar.domain.public_links.entities import PublicEnrollmentLink


class PublicEnrollmentLinkRepository(Protocol):
    """Contrato minimo esperado de um repositorio de links publicos."""

    def list_all(self) -> Sequence[PublicEnrollmentLink]:
        """Retorna todos os links publicos cadastrados."""

    def get_by_id(self, link_id: str) -> PublicEnrollmentLink | None:
        """Busca um link publico por identificador."""

    def get_by_token(self, token: str) -> PublicEnrollmentLink | None:
        """Busca um link publico pelo token exposto ao responsavel."""

    def add(self, public_link: PublicEnrollmentLink) -> PublicEnrollmentLink:
        """Persiste um novo link publico."""

