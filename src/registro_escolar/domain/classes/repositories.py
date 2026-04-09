"""Contratos de persistencia para o contexto de turmas."""

from collections.abc import Sequence
from typing import Protocol

from registro_escolar.domain.classes.entities import SchoolClass


class SchoolClassRepository(Protocol):
    """Contrato minimo esperado de um repositorio de turmas."""

    def list_all(self) -> Sequence[SchoolClass]:
        """Retorna todas as turmas cadastradas."""

    def get_by_id(self, class_id: str) -> SchoolClass | None:
        """Busca uma turma por identificador."""

    def get_by_scope(
        self,
        school_id: str,
        academic_term_id: str,
        normalized_name: str,
    ) -> SchoolClass | None:
        """Busca turma pela combinacao escola + periodo + nome."""

    def add(self, school_class: SchoolClass) -> SchoolClass:
        """Persiste uma nova turma."""
