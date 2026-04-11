"""Repositorio em memoria para o contexto de formularios."""

from __future__ import annotations

from collections.abc import Sequence

from registro_escolar.domain.forms.entities import EnrollmentForm


class InMemoryEnrollmentFormRepository:
    """Persistencia temporaria em memoria para formularios."""

    def __init__(self) -> None:
        """Inicializa a colecao vazia de formularios."""

        self._forms: list[EnrollmentForm] = []

    def list_all(self) -> Sequence[EnrollmentForm]:
        """Retorna todos os formularios cadastrados."""

        return tuple(self._forms)

    def get_by_id(self, form_id: str) -> EnrollmentForm | None:
        """Busca um formulario pelo identificador."""

        return next((item for item in self._forms if item.id == form_id), None)

    def get_by_scope(
        self,
        school_id: str,
        academic_term_id: str,
        normalized_name: str,
    ) -> EnrollmentForm | None:
        """Busca um formulario por escopo e nome normalizado."""

        return next(
            (
                item
                for item in self._forms
                if item.school_id == school_id
                and item.academic_term_id == academic_term_id
                and self._normalize_name(item.name) == normalized_name
            ),
            None,
        )

    def add(self, enrollment_form: EnrollmentForm) -> EnrollmentForm:
        """Adiciona um novo formulario na colecao."""

        self._forms.append(enrollment_form)
        return enrollment_form

    @staticmethod
    def _normalize_name(value: str) -> str:
        """Normaliza o nome para comparacoes previsiveis."""

        return " ".join(value.lower().split())

