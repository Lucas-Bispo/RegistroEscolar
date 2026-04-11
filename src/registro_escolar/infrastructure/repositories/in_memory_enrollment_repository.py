"""Repositorio em memoria para o contexto de inscricoes publicas."""

from __future__ import annotations

from collections.abc import Sequence

from registro_escolar.domain.enrollments.entities import Enrollment


class InMemoryEnrollmentRepository:
    """Persistencia temporaria em memoria para inscricoes."""

    def __init__(self) -> None:
        """Inicializa a colecao vazia de inscricoes."""

        self._enrollments: list[Enrollment] = []

    def list_all(self) -> Sequence[Enrollment]:
        """Retorna todas as inscricoes cadastradas."""

        return tuple(self._enrollments)

    def add(self, enrollment: Enrollment) -> Enrollment:
        """Adiciona uma nova inscricao na colecao."""

        self._enrollments.append(enrollment)
        return enrollment

    def count_by_public_link_id(self, public_link_id: str) -> int:
        """Conta quantas inscricoes estao associadas a um link."""

        return sum(
            1 for item in self._enrollments if item.public_link_id == public_link_id
        )
