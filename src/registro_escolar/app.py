"""Bootstrap da aplicacao FastAPI."""

import uvicorn
from fastapi import APIRouter, FastAPI

from registro_escolar.api.router import api_router
from registro_escolar.core.config import get_settings
from registro_escolar.core.logging import configure_logging


def create_app() -> FastAPI:
    """Cria e configura a instancia principal da aplicacao.

    Returns:
        FastAPI: Aplicacao HTTP pronta para receber rotas.
    """
    settings = get_settings()

    # O logging e configurado no bootstrap para que toda a aplicacao
    # utilize o mesmo padrao desde o inicio da execucao.
    configure_logging(log_level=settings.log_level)

    app = FastAPI(
        title=settings.app_name,
        docs_url=settings.docs_url,
        redoc_url=settings.redoc_url,
    )
    app.include_router(build_root_router())
    app.include_router(api_router)
    return app


def build_root_router() -> APIRouter:
    """Cria uma rota raiz com links de navegacao rapida.

    Embora simples, esta rota melhora a experiencia de quem esta
    acompanhando o projeto em localhost, porque aponta para healthcheck
    e documentacao sem exigir conhecimento previo da estrutura da API.
    """

    root_router = APIRouter()

    @root_router.get("/", tags=["meta"], summary="Apresenta links uteis da aplicacao")
    def root() -> dict[str, str]:
        return {
            "name": "RegistroEscolar",
            "docs": "/docs",
            "health": "/api/v1/health",
            "schools": "/api/v1/schools",
        }

    return root_router


def run() -> None:
    """Executa o servidor de desenvolvimento local."""
    settings = get_settings()
    uvicorn.run(
        "registro_escolar.app:create_app",
        factory=True,
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
    )
