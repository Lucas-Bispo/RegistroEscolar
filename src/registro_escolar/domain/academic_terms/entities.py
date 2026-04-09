"""Entidades de dominio do contexto de periodos letivos."""

from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from uuid import uuid4


@dataclass(slots=True)
class AcademicTerm:
    """Representa um periodo letivo configurado pelo admin."""

    name: str
    start_date: date
    end_date: date
    is_active: bool = True
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
