"""Servicos de aplicacao relacionados a periodos letivos."""

from collections.abc import Sequence
from datetime import date

from registro_escolar.domain.academic_terms.entities import AcademicTerm
from registro_escolar.domain.academic_terms.repositories import AcademicTermRepository


class AcademicTermAlreadyExistsError(ValueError):
    """Erro levantado quando tentamos cadastrar um periodo duplicado."""


class AcademicTermNotFoundError(LookupError):
    """Erro levantado quando um periodo nao e encontrado."""


class InvalidAcademicTermRangeError(ValueError):
    """Erro levantado quando a data inicial e maior que a final."""


class AcademicTermService:
    """Orquestra os casos de uso do contexto de periodos letivos."""

    def __init__(self, repository: AcademicTermRepository) -> None:
        self._repository = repository

    def list_terms(self) -> Sequence[AcademicTerm]:
        """Lista todos os periodos letivos cadastrados."""

        return self._repository.list_all()

    def get_term(self, term_id: str) -> AcademicTerm:
        """Busca um periodo especifico pelo identificador."""

        academic_term = self._repository.get_by_id(term_id)
        if academic_term is None:
            msg = "Periodo letivo nao encontrado."
            raise AcademicTermNotFoundError(msg)
        return academic_term

    def create_term(
        self,
        name: str,
        start_date: date,
        end_date: date,
        is_active: bool,
    ) -> AcademicTerm:
        """Cria um novo periodo com validacoes basicas de negocio."""

        if start_date > end_date:
            msg = "A data inicial nao pode ser maior que a data final."
            raise InvalidAcademicTermRangeError(msg)

        normalized_name = self._normalize_name(name)
        existing_term = self._repository.get_by_normalized_name(normalized_name)
        if existing_term is not None:
            msg = "Ja existe um periodo letivo com este nome."
            raise AcademicTermAlreadyExistsError(msg)

        academic_term = AcademicTerm(
            name=name.strip(),
            start_date=start_date,
            end_date=end_date,
            is_active=is_active,
        )
        return self._repository.add(academic_term)

    @staticmethod
    def _normalize_name(value: str) -> str:
        """Normaliza o nome para comparacoes simples de unicidade."""

        return " ".join(value.lower().split())
