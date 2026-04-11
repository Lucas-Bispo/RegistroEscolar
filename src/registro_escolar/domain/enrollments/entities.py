"""Entidades de dominio do contexto de inscricoes publicas."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4


@dataclass(slots=True, frozen=True)
class EnrollmentAnswer:
    """Representa uma resposta enviada para um campo do formulario."""

    field_order: int
    field_label: str
    value: str


@dataclass(slots=True)
class Enrollment:
    """Representa uma inscricao publica submetida por um responsavel."""

    school_id: str
    academic_term_id: str
    class_id: str
    form_id: str
    public_link_id: str
    protocol: str
    answers: tuple[EnrollmentAnswer, ...]
    status: str = "submitted"
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
