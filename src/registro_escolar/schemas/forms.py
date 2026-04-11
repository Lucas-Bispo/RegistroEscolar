"""Schemas Pydantic do contexto de formularios."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class FormFieldCreate(BaseModel):
    """Payload de entrada para um campo do formulario."""

    label: str = Field(min_length=2, max_length=120)
    field_type: Literal["text", "date", "email", "phone", "select", "upload"]
    required: bool = True
    placeholder: str = Field(default="", max_length=160)
    options: list[str] = Field(default_factory=list)
    order: int = Field(ge=1, le=100)

    @model_validator(mode="after")
    def validate_options(self) -> "FormFieldCreate":
        """Aplica regras basicas de coerencia entre tipo e opcoes."""

        if self.field_type == "select" and not self.options:
            msg = "Campos do tipo select precisam informar opcoes."
            raise ValueError(msg)
        if self.field_type != "select" and self.options:
            msg = "Somente campos do tipo select podem informar opcoes."
            raise ValueError(msg)
        return self


class EnrollmentFormCreate(BaseModel):
    """Payload de entrada para criacao de formulario."""

    school_id: str
    academic_term_id: str
    name: str = Field(min_length=3, max_length=120)
    description: str = Field(default="", max_length=400)
    fields: list[FormFieldCreate] = Field(min_length=1, max_length=30)
    is_published: bool = False


class FormFieldResponse(BaseModel):
    """Payload padronizado de saida para um campo do formulario."""

    model_config = ConfigDict(from_attributes=True)

    label: str
    field_type: str
    required: bool
    placeholder: str
    options: tuple[str, ...]
    order: int


class EnrollmentFormResponse(BaseModel):
    """Payload padronizado de saida para um formulario."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    school_id: str
    academic_term_id: str
    name: str
    description: str
    fields: list[FormFieldResponse]
    is_published: bool
    version: int
    created_at: datetime

