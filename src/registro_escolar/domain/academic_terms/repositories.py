"""Contratos de persistencia para o contexto de periodos letivos."""

from collections.abc import Sequence
from typing import Protocol

from registro_escolar.domain.academic_terms.entities import AcademicTerm


class AcademicTermRepository(Protocol):
    """Contrato minimo esperado de um repositorio de periodos letivos."""

    def list_all(self) -> Sequence[AcademicTerm]:
        """Retorna todos os periodos."""

    def get_by_id(self, term_id: str) -> AcademicTerm | None:
        """Busca um periodo por identificador."""

    def get_by_normalized_name(self, normalized_name: str) -> AcademicTerm | None:
        """Busca um periodo pelo nome normalizado."""

    def add(self, academic_term: AcademicTerm) -> AcademicTerm:
        """Persiste um novo periodo letivo."""
