"""Servicos de aplicacao relacionados a turmas e vagas."""

from collections.abc import Sequence

from registro_escolar.domain.academic_terms.repositories import AcademicTermRepository
from registro_escolar.domain.classes.entities import SchoolClass
from registro_escolar.domain.classes.repositories import SchoolClassRepository
from registro_escolar.domain.schools.repositories import SchoolRepository


class SchoolClassAlreadyExistsError(ValueError):
    """Erro levantado quando tentamos cadastrar uma turma duplicada."""


class SchoolClassNotFoundError(LookupError):
    """Erro levantado quando uma turma nao e encontrada."""


class InvalidClassCapacityError(ValueError):
    """Erro levantado quando a capacidade informada e invalida."""


class InvalidClassRelationError(ValueError):
    """Erro levantado quando escola ou periodo nao existem."""


class SchoolClassService:
    """Orquestra os casos de uso do contexto de turmas."""

    def __init__(
        self,
        class_repository: SchoolClassRepository,
        school_repository: SchoolRepository,
        academic_term_repository: AcademicTermRepository,
    ) -> None:
        self._class_repository = class_repository
        self._school_repository = school_repository
        self._academic_term_repository = academic_term_repository

    def list_classes(self) -> Sequence[SchoolClass]:
        """Lista todas as turmas cadastradas."""

        return self._class_repository.list_all()

    def get_class(self, class_id: str) -> SchoolClass:
        """Busca uma turma pelo identificador."""

        school_class = self._class_repository.get_by_id(class_id)
        if school_class is None:
            msg = "Turma nao encontrada."
            raise SchoolClassNotFoundError(msg)
        return school_class

    def create_class(
        self,
        school_id: str,
        academic_term_id: str,
        name: str,
        shift: str,
        capacity: int,
        is_active: bool,
    ) -> SchoolClass:
        """Cria uma nova turma com validacoes basicas de negocio."""

        if capacity <= 0:
            msg = "A capacidade da turma deve ser maior que zero."
            raise InvalidClassCapacityError(msg)

        school = self._school_repository.get_by_id(school_id)
        academic_term = self._academic_term_repository.get_by_id(academic_term_id)
        if school is None or academic_term is None:
            msg = "A turma precisa estar vinculada a uma escola e a um periodo valido."
            raise InvalidClassRelationError(msg)

        normalized_name = self._normalize_name(name)
        existing_class = self._class_repository.get_by_scope(
            school_id=school_id,
            academic_term_id=academic_term_id,
            normalized_name=normalized_name,
        )
        if existing_class is not None:
            msg = "Ja existe uma turma com este nome nessa escola e periodo."
            raise SchoolClassAlreadyExistsError(msg)

        school_class = SchoolClass(
            school_id=school_id,
            academic_term_id=academic_term_id,
            name=name.strip(),
            shift=shift.strip(),
            capacity=capacity,
            is_active=is_active,
        )
        return self._class_repository.add(school_class)

    @staticmethod
    def _normalize_name(value: str) -> str:
        """Normaliza o nome para comparacoes simples de unicidade."""

        return " ".join(value.lower().split())
