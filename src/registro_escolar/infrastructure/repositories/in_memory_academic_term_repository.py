"""Repositorio em memoria para o contexto de periodos letivos."""

from __future__ import annotations

from collections.abc import Sequence
from datetime import date

from registro_escolar.domain.academic_terms.entities import AcademicTerm


class InMemoryAcademicTermRepository:
    """Persistencia temporaria em memoria para periodos letivos."""

    def __init__(self) -> None:
        """Inicializa o repositorio com campanhas de exemplo."""

        self._academic_terms: list[AcademicTerm] = [
            AcademicTerm(
                name="Matricula 2026",
                start_date=date(2026, 1, 5),
                end_date=date(2026, 12, 20),
                is_active=True,
            ),
            AcademicTerm(
                name="Matricula 2027",
                start_date=date(2027, 1, 12),
                end_date=date(2027, 12, 18),
                is_active=False,
            ),
        ]

    def list_all(self) -> Sequence[AcademicTerm]:
        """Retorna uma copia dos periodos configurados."""

        return tuple(self._academic_terms)

    def get_by_id(self, term_id: str) -> AcademicTerm | None:
        """Busca um periodo pelo identificador."""

        return next((term for term in self._academic_terms if term.id == term_id), None)

    def get_by_normalized_name(self, normalized_name: str) -> AcademicTerm | None:
        """Busca um periodo pelo nome normalizado."""

        return next(
            (
                term
                for term in self._academic_terms
                if self._normalize_name(term.name) == normalized_name
            ),
            None,
        )

    def add(self, academic_term: AcademicTerm) -> AcademicTerm:
        """Adiciona um novo periodo na colecao."""

        self._academic_terms.append(academic_term)
        return academic_term

    @staticmethod
    def _normalize_name(value: str) -> str:
        """Normaliza o nome para comparacoes previsiveis."""

        return " ".join(value.lower().split())
