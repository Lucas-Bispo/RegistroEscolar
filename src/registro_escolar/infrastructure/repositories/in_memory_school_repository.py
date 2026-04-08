"""Repositorio em memoria para o contexto de escolas."""

from __future__ import annotations

from collections.abc import Sequence

from registro_escolar.domain.schools.entities import School


class InMemorySchoolRepository:
    """Implementa persistencia temporaria em memoria.

    Esta classe existe para validar a arquitetura antes da integracao com
    banco de dados. Em producao, ela sera substituida por uma implementacao
    real, mas mantendo o mesmo contrato esperado pelo servico.
    """

    def __init__(self) -> None:
        """Inicializa o repositorio com dados de exemplo."""
        self._schools: list[School] = [
            School(name="Colegio Horizonte", city="Sao Paulo", state="SP"),
            School(name="Escola Aurora", city="Campinas", state="SP"),
        ]

    def list_all(self) -> Sequence[School]:
        """Retorna uma copia da lista de escolas em memoria."""
        return tuple(self._schools)

    def get_by_id(self, school_id: str) -> School | None:
        """Busca uma escola pelo identificador."""
        return next(
            (school for school in self._schools if school.id == school_id),
            None,
        )

    def get_by_normalized_name(self, normalized_name: str) -> School | None:
        """Busca uma escola pelo nome normalizado."""
        return next(
            (
                school
                for school in self._schools
                if self._normalize_name(school.name) == normalized_name
            ),
            None,
        )

    def add(self, school: School) -> School:
        """Adiciona uma nova escola na colecao em memoria."""
        self._schools.append(school)
        return school

    @staticmethod
    def _normalize_name(value: str) -> str:
        """Normaliza o nome para comparacoes simples e previsiveis."""
        return " ".join(value.lower().split())
