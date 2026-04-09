"""Dependencias compartilhadas entre camadas de apresentacao."""

from registro_escolar.domain.academic_terms.repositories import AcademicTermRepository
from registro_escolar.domain.schools.repositories import SchoolRepository
from registro_escolar.infrastructure.repositories import (
    in_memory_academic_term_repository,
)
from registro_escolar.infrastructure.repositories.in_memory_school_repository import (
    InMemorySchoolRepository,
)
from registro_escolar.services.academic_terms import AcademicTermService
from registro_escolar.services.auth import AdminAuthService
from registro_escolar.services.schools import SchoolService

_school_repository = InMemorySchoolRepository()
_academic_term_repository = (
    in_memory_academic_term_repository.InMemoryAcademicTermRepository()
)


def get_school_repository() -> SchoolRepository:
    """Retorna a implementacao atual do repositorio de escolas."""

    return _school_repository


def get_academic_term_repository() -> AcademicTermRepository:
    """Retorna a implementacao atual do repositorio de periodos letivos."""

    return _academic_term_repository


def get_school_service() -> SchoolService:
    """Retorna o servico de escolas com a implementacao atual."""

    return SchoolService(repository=get_school_repository())


def get_academic_term_service() -> AcademicTermService:
    """Retorna o servico de periodos letivos com a implementacao atual."""

    return AcademicTermService(repository=get_academic_term_repository())


def get_admin_auth_service() -> AdminAuthService:
    """Retorna o servico de autenticacao administrativa."""

    return AdminAuthService()
