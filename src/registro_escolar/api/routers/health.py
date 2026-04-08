"""Rotas simples de diagnostico da aplicacao."""

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health", summary="Verifica a saude basica da aplicacao")
def healthcheck() -> dict[str, str]:
    """Retorna um payload simples para validacao operacional.

    Returns:
        dict[str, str]: Estado minimo da aplicacao.
    """
    return {"status": "ok"}
