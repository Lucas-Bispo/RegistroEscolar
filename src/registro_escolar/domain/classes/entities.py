"""Entidades de dominio do contexto de turmas."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4


@dataclass(slots=True)
class SchoolClass:
    """Representa uma turma configurada pelo admin."""

    school_id: str
    academic_term_id: str
    name: str
    shift: str
    capacity: int
    is_active: bool = True
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
