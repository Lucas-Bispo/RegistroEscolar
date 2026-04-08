"""Servicos de aplicacao relacionados ao contexto de escolas."""

from collections.abc import Sequence

from registro_escolar.domain.schools.entities import School
from registro_escolar.domain.schools.repositories import SchoolRepository


class SchoolAlreadyExistsError(ValueError):
    """Erro levantado quando tentamos cadastrar uma escola duplicada."""


class SchoolNotFoundError(LookupError):
    """Erro levantado quando uma escola nao e encontrada."""


class SchoolService:
    """Orquestra os casos de uso do contexto de escolas.

    O servico e uma boa escolha aqui porque centraliza a regra de negocio
    e impede que a rota HTTP conheca detalhes de persistencia.
    """

    def __init__(self, repository: SchoolRepository) -> None:
        self._repository = repository

    def list_schools(self) -> Sequence[School]:
        """Lista todas as escolas disponiveis."""
        return self._repository.list_all()

    def get_school(self, school_id: str) -> School:
        """Busca uma escola por identificador.

        Raises:
            SchoolNotFoundError: Quando o identificador nao existe.
        """
        school = self._repository.get_by_id(school_id)
        if school is None:
            msg = "Escola nao encontrada."
            raise SchoolNotFoundError(msg)
        return school

    def create_school(self, name: str, city: str, state: str) -> School:
        """Cria uma nova escola com validacoes basicas de negocio.

        Raises:
            SchoolAlreadyExistsError: Quando ja existe escola com o mesmo nome.
        """
        normalized_name = self._normalize_name(name)
        existing_school = self._repository.get_by_normalized_name(normalized_name)
        if existing_school is not None:
            msg = "Ja existe uma escola cadastrada com este nome."
            raise SchoolAlreadyExistsError(msg)

        school = School(
            name=name.strip(),
            city=city.strip(),
            state=state.strip().upper(),
        )
        return self._repository.add(school)

    @staticmethod
    def _normalize_name(value: str) -> str:
        """Normaliza o nome para comparacoes simples de unicidade."""
        return " ".join(value.lower().split())
