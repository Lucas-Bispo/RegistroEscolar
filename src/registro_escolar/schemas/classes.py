"""Schemas Pydantic do contexto de turmas."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SchoolClassCreate(BaseModel):
    """Payload de entrada para criacao de turma."""

    school_id: str
    academic_term_id: str
    name: str = Field(min_length=2, max_length=120)
    shift: str = Field(min_length=2, max_length=40)
    capacity: int = Field(gt=0, le=500)
    is_active: bool = True


class SchoolClassResponse(BaseModel):
    """Payload padronizado de saida para uma turma."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    school_id: str
    academic_term_id: str
    name: str
    shift: str
    capacity: int
    is_active: bool
    created_at: datetime
