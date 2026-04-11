"""Schemas Pydantic do contexto de links publicos."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PublicEnrollmentLinkCreate(BaseModel):
    """Payload de entrada para criacao de link publico."""

    school_id: str
    academic_term_id: str
    form_id: str
    expires_at: datetime
    max_submissions: int = Field(gt=0, le=10000)
    is_active: bool = True


class PublicEnrollmentLinkResponse(BaseModel):
    """Payload padronizado de saida para um link publico."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    school_id: str
    academic_term_id: str
    form_id: str
    token: str
    expires_at: datetime
    max_submissions: int
    is_active: bool
    created_at: datetime

