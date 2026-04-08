"""Rotas basicas da API versionada."""

from fastapi import APIRouter

router = APIRouter(tags=["meta"])


@router.get("/", summary="Retorna informacoes basicas da API")
def api_root() -> dict[str, str]:
    """Apresenta um resumo simples da API atual."""
    return {
        "name": "RegistroEscolar API",
        "version": "v1",
        "docs": "/docs",
    }
