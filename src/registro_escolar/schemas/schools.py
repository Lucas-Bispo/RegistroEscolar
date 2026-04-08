"""Schemas Pydantic do contexto de escolas."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SchoolCreate(BaseModel):
    """Payload de entrada para criacao de escola."""

    name: str = Field(min_length=3, max_length=120)
    city: str = Field(min_length=2, max_length=80)
    state: str = Field(min_length=2, max_length=2)


class SchoolResponse(BaseModel):
    """Payload padronizado de saida para uma escola."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    city: str
    state: str
    is_active: bool
    created_at: datetime
