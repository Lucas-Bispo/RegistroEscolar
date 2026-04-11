"""Dependencias compartilhadas entre camadas de apresentacao."""

from registro_escolar.domain.academic_terms.repositories import AcademicTermRepository
from registro_escolar.domain.classes.repositories import SchoolClassRepository
from registro_escolar.domain.enrollments.repositories import EnrollmentRepository
from registro_escolar.domain.forms.repositories import EnrollmentFormRepository
from registro_escolar.domain.public_links.repositories import (
    PublicEnrollmentLinkRepository,
)
from registro_escolar.domain.schools.repositories import SchoolRepository
from registro_escolar.infrastructure.repositories import (
    in_memory_academic_term_repository,
    in_memory_enrollment_form_repository,
    in_memory_enrollment_repository,
    in_memory_public_enrollment_link_repository,
    in_memory_school_class_repository,
)
from registro_escolar.infrastructure.repositories.in_memory_school_repository import (
    InMemorySchoolRepository,
)
from registro_escolar.services.academic_terms import AcademicTermService
from registro_escolar.services.auth import AdminAuthService
from registro_escolar.services.classes import SchoolClassService
from registro_escolar.services.enrollments import EnrollmentService
from registro_escolar.services.forms import EnrollmentFormService
from registro_escolar.services.public_links import PublicEnrollmentLinkService
from registro_escolar.services.schools import SchoolService

_school_repository = InMemorySchoolRepository()
_academic_term_repository = (
    in_memory_academic_term_repository.InMemoryAcademicTermRepository()
)
_school_class_repository = (
    in_memory_school_class_repository.InMemorySchoolClassRepository()
)
_enrollment_form_repository = (
    in_memory_enrollment_form_repository.InMemoryEnrollmentFormRepository()
)
_public_enrollment_link_repository = (
    in_memory_public_enrollment_link_repository.InMemoryPublicEnrollmentLinkRepository()
)
_enrollment_repository = (
    in_memory_enrollment_repository.InMemoryEnrollmentRepository()
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


def get_school_class_repository() -> SchoolClassRepository:
    """Retorna a implementacao atual do repositorio de turmas."""

    return _school_class_repository


def get_academic_term_service() -> AcademicTermService:
    """Retorna o servico de periodos letivos com a implementacao atual."""

    return AcademicTermService(repository=get_academic_term_repository())


def get_school_class_service() -> SchoolClassService:
    """Retorna o servico de turmas com as dependencias atuais."""

    return SchoolClassService(
        class_repository=get_school_class_repository(),
        school_repository=get_school_repository(),
        academic_term_repository=get_academic_term_repository(),
    )


def get_enrollment_form_repository() -> EnrollmentFormRepository:
    """Retorna a implementacao atual do repositorio de formularios."""

    return _enrollment_form_repository


def get_enrollment_form_service() -> EnrollmentFormService:
    """Retorna o servico de formularios com as dependencias atuais."""

    return EnrollmentFormService(
        form_repository=get_enrollment_form_repository(),
        school_repository=get_school_repository(),
        academic_term_repository=get_academic_term_repository(),
    )


def get_public_enrollment_link_repository() -> PublicEnrollmentLinkRepository:
    """Retorna a implementacao atual do repositorio de links publicos."""

    return _public_enrollment_link_repository


def get_public_enrollment_link_service() -> PublicEnrollmentLinkService:
    """Retorna o servico de links publicos com as dependencias atuais."""

    return PublicEnrollmentLinkService(
        link_repository=get_public_enrollment_link_repository(),
        school_repository=get_school_repository(),
        academic_term_repository=get_academic_term_repository(),
        form_repository=get_enrollment_form_repository(),
    )


def get_enrollment_repository() -> EnrollmentRepository:
    """Retorna a implementacao atual do repositorio de inscricoes."""

    return _enrollment_repository


def get_enrollment_service() -> EnrollmentService:
    """Retorna o servico de inscricoes com as dependencias atuais."""

    return EnrollmentService(
        enrollment_repository=get_enrollment_repository(),
        public_link_repository=get_public_enrollment_link_repository(),
        school_repository=get_school_repository(),
        academic_term_repository=get_academic_term_repository(),
        class_repository=get_school_class_repository(),
        form_repository=get_enrollment_form_repository(),
    )


def get_admin_auth_service() -> AdminAuthService:
    """Retorna o servico de autenticacao administrativa."""

    return AdminAuthService()
