"""Repositorio em memoria para o contexto de links publicos."""

from __future__ import annotations

from collections.abc import Sequence

from registro_escolar.domain.public_links.entities import PublicEnrollmentLink


class InMemoryPublicEnrollmentLinkRepository:
    """Persistencia temporaria em memoria para links publicos."""

    def __init__(self) -> None:
        """Inicializa a colecao vazia de links publicos."""

        self._links: list[PublicEnrollmentLink] = []

    def list_all(self) -> Sequence[PublicEnrollmentLink]:
        """Retorna todos os links publicos cadastrados."""

        return tuple(self._links)

    def get_by_id(self, link_id: str) -> PublicEnrollmentLink | None:
        """Busca um link publico pelo identificador."""

        return next((item for item in self._links if item.id == link_id), None)

    def get_by_token(self, token: str) -> PublicEnrollmentLink | None:
        """Busca um link publico pelo token."""

        return next((item for item in self._links if item.token == token), None)

    def add(self, public_link: PublicEnrollmentLink) -> PublicEnrollmentLink:
        """Adiciona um novo link publico na colecao."""

        self._links.append(public_link)
        return public_link

