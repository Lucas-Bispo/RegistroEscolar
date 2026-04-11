"""Entidades de dominio do contexto de links publicos."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4


@dataclass(slots=True)
class PublicEnrollmentLink:
    """Representa um link publico para uma campanha de matricula."""

    school_id: str
    academic_term_id: str
    form_id: str
    token: str
    expires_at: datetime
    max_submissions: int
    is_active: bool = True
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

