"""Repositorio em memoria para o contexto de turmas."""

from __future__ import annotations

from collections.abc import Sequence

from registro_escolar.domain.classes.entities import SchoolClass


class InMemorySchoolClassRepository:
    """Persistencia temporaria em memoria para turmas."""

    def __init__(self) -> None:
        """Inicializa a colecao vazia de turmas."""

        self._classes: list[SchoolClass] = []

    def list_all(self) -> Sequence[SchoolClass]:
        """Retorna todas as turmas cadastradas."""

        return tuple(self._classes)

    def get_by_id(self, class_id: str) -> SchoolClass | None:
        """Busca uma turma pelo identificador."""

        return next((item for item in self._classes if item.id == class_id), None)

    def get_by_scope(
        self,
        school_id: str,
        academic_term_id: str,
        normalized_name: str,
    ) -> SchoolClass | None:
        """Busca uma turma por escopo e nome normalizado."""

        return next(
            (
                item
                for item in self._classes
                if item.school_id == school_id
                and item.academic_term_id == academic_term_id
                and self._normalize_name(item.name) == normalized_name
            ),
            None,
        )

    def add(self, school_class: SchoolClass) -> SchoolClass:
        """Adiciona uma nova turma na colecao."""

        self._classes.append(school_class)
        return school_class

    @staticmethod
    def _normalize_name(value: str) -> str:
        """Normaliza o nome para comparacoes previsiveis."""

        return " ".join(value.lower().split())
