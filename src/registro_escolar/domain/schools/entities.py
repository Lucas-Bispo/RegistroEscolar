"""Entidades de dominio do contexto de escolas."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4


@dataclass(slots=True)
class School:
    """Representa uma escola dentro do dominio da aplicacao.

    A escolha por ``dataclass`` faz sentido aqui porque:

    - queremos uma estrutura de dados simples e legivel;
    - o dominio ainda nao exige comportamento complexo de ORM;
    - mantemos tipagem explicita e boa ergonomia de manutencao.
    """

    name: str
    city: str
    state: str
    is_active: bool = True
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
