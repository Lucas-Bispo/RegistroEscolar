"""Contratos de persistencia para o contexto de inscricoes publicas."""

from collections.abc import Sequence
from typing import Protocol

from registro_escolar.domain.enrollments.entities import Enrollment


class EnrollmentRepository(Protocol):
    """Contrato minimo esperado de um repositorio de inscricoes."""

    def list_all(self) -> Sequence[Enrollment]:
        """Retorna todas as inscricoes cadastradas."""

    def add(self, enrollment: Enrollment) -> Enrollment:
        """Persiste uma nova inscricao."""

    def count_by_public_link_id(self, public_link_id: str) -> int:
        """Conta quantas inscricoes ja foram recebidas em um link."""
