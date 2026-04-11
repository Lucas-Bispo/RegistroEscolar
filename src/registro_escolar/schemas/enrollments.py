"""Schemas Pydantic do contexto de inscricoes publicas."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator


class EnrollmentAnswerCreate(BaseModel):
    """Payload de entrada para uma resposta do formulario."""

    order: int = Field(ge=1, le=100)
    value: str = Field(default="", max_length=500)


class PublicEnrollmentCreate(BaseModel):
    """Payload de entrada para uma inscricao publica."""

    token: str = Field(min_length=10, max_length=255)
    class_id: str
    answers: list[EnrollmentAnswerCreate] = Field(min_length=1, max_length=30)

    @model_validator(mode="after")
    def validate_unique_orders(self) -> "PublicEnrollmentCreate":
        """Impede respostas duplicadas para o mesmo campo."""

        orders = [item.order for item in self.answers]
        if len(orders) != len(set(orders)):
            msg = "Nao e permitido informar o mesmo campo mais de uma vez."
            raise ValueError(msg)
        return self


class EnrollmentAnswerResponse(BaseModel):
    """Payload padronizado de saida para uma resposta registrada."""

    model_config = ConfigDict(from_attributes=True)

    field_order: int
    field_label: str
    value: str


class EnrollmentResponse(BaseModel):
    """Payload padronizado de saida para uma inscricao."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    school_id: str
    academic_term_id: str
    class_id: str
    form_id: str
    public_link_id: str
    protocol: str
    status: str
    answers: list[EnrollmentAnswerResponse]
    created_at: datetime
