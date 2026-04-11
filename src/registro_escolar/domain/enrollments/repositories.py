"""Contratos de persistencia para o contexto de inscricoes publicas."""

from collections.abc import Sequence
from typing import Protocol

from registro_escolar.domain.enrollments.entities import Enrollment


class EnrollmentRepository(Protocol):
    """Contrato minimo esperado de um repositorio de inscricoes."""

    def list_all(self) -> Sequence[Enrollment]:
        """Retorna todas as inscricoes cadastradas."""

    def get_by_id(self, enrollment_id: str) -> Enrollment | None:
        """Busca uma inscricao por identificador."""

    def add(self, enrollment: Enrollment) -> Enrollment:
        """Persiste uma nova inscricao."""

    def update(self, enrollment: Enrollment) -> Enrollment:
        """Atualiza uma inscricao ja persistida."""

    def count_by_public_link_id(self, public_link_id: str) -> int:
        """Conta quantas inscricoes ja foram recebidas em um link."""

    def count_by_class_id_and_status(self, class_id: str, status: str) -> int:
        """Conta inscricoes por turma e status."""
