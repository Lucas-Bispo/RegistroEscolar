"""Dependencias compartilhadas entre camadas de apresentacao."""

from registro_escolar.domain.schools.repositories import SchoolRepository
from registro_escolar.infrastructure.repositories.in_memory_school_repository import (
    InMemorySchoolRepository,
)
from registro_escolar.services.auth import AdminAuthService
from registro_escolar.services.schools import SchoolService

_school_repository = InMemorySchoolRepository()


def get_school_repository() -> SchoolRepository:
    """Retorna a implementacao atual do repositorio de escolas."""

    return _school_repository


def get_school_service() -> SchoolService:
    """Retorna o servico de escolas com a implementacao atual."""

    return SchoolService(repository=get_school_repository())


def get_admin_auth_service() -> AdminAuthService:
    """Retorna o servico de autenticacao administrativa."""

    return AdminAuthService()
