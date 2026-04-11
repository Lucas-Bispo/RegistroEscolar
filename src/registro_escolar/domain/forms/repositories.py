"""Contratos de persistencia para o contexto de formularios."""

from collections.abc import Sequence
from typing import Protocol

from registro_escolar.domain.forms.entities import EnrollmentForm


class EnrollmentFormRepository(Protocol):
    """Contrato minimo esperado de um repositorio de formularios."""

    def list_all(self) -> Sequence[EnrollmentForm]:
        """Retorna todos os formularios cadastrados."""

    def get_by_id(self, form_id: str) -> EnrollmentForm | None:
        """Busca um formulario por identificador."""

    def get_by_scope(
        self,
        school_id: str,
        academic_term_id: str,
        normalized_name: str,
    ) -> EnrollmentForm | None:
        """Busca um formulario pela combinacao escola + periodo + nome."""

    def add(self, enrollment_form: EnrollmentForm) -> EnrollmentForm:
        """Persiste um novo formulario."""

