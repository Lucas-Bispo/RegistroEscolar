"""Contratos de persistencia para o contexto de escolas."""

from collections.abc import Sequence
from typing import Protocol

from registro_escolar.domain.schools.entities import School


class SchoolRepository(Protocol):
    """Define o contrato minimo esperado de um repositorio de escolas.

    O uso de ``Protocol`` ajuda a aplicar um estilo proximo de
    inversao de dependencia. O servico depende do contrato esperado,
    nao da implementacao concreta em memoria ou futura implementacao
    com banco de dados.
    """

    def list_all(self) -> Sequence[School]:
        """Retorna todas as escolas disponiveis."""

    def get_by_id(self, school_id: str) -> School | None:
        """Busca uma escola por identificador."""

    def get_by_normalized_name(self, normalized_name: str) -> School | None:
        """Busca uma escola pelo nome normalizado."""

    def add(self, school: School) -> School:
        """Persiste uma nova escola."""
