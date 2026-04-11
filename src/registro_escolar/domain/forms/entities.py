"""Entidades de dominio do contexto de formularios."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4


@dataclass(slots=True, frozen=True)
class FormField:
    """Representa um campo configuravel do formulario."""

    label: str
    field_type: str
    required: bool = True
    placeholder: str = ""
    options: tuple[str, ...] = ()
    order: int = 1


@dataclass(slots=True)
class EnrollmentForm:
    """Representa um formulario configurado para uma campanha."""

    school_id: str
    academic_term_id: str
    name: str
    description: str
    fields: tuple[FormField, ...]
    is_published: bool = False
    version: int = 1
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

