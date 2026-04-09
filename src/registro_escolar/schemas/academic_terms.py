"""Schemas Pydantic do contexto de periodos letivos."""

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class AcademicTermCreate(BaseModel):
    """Payload de entrada para criacao de periodo letivo."""

    name: str = Field(min_length=3, max_length=120)
    start_date: date
    end_date: date
    is_active: bool = True


class AcademicTermResponse(BaseModel):
    """Payload padronizado de saida para um periodo letivo."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    start_date: date
    end_date: date
    is_active: bool
    created_at: datetime
