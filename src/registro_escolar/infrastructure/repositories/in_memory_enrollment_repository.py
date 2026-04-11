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

    def get_by_id(self, enrollment_id: str) -> Enrollment | None:
        """Busca uma inscricao pelo identificador."""

        return next((item for item in self._enrollments if item.id == enrollment_id), None)

    def add(self, enrollment: Enrollment) -> Enrollment:
        """Adiciona uma nova inscricao na colecao."""

        self._enrollments.append(enrollment)
        return enrollment

    def update(self, enrollment: Enrollment) -> Enrollment:
        """Atualiza uma inscricao ja existente na colecao."""

        for index, current_item in enumerate(self._enrollments):
            if current_item.id == enrollment.id:
                self._enrollments[index] = enrollment
                return enrollment
        self._enrollments.append(enrollment)
        return enrollment

    def count_by_public_link_id(self, public_link_id: str) -> int:
        """Conta quantas inscricoes estao associadas a um link."""

        return sum(
            1 for item in self._enrollments if item.public_link_id == public_link_id
        )

    def count_by_class_id_and_status(self, class_id: str, status: str) -> int:
        """Conta inscricoes por turma considerando um status especifico."""

        return sum(
            1
            for item in self._enrollments
            if item.class_id == class_id and item.status == status
        )
