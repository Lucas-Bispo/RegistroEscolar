"""Bootstrap da aplicacao FastAPI."""

from fastapi import FastAPI
import uvicorn

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

    app = FastAPI(title=settings.app_name)
    app.include_router(api_router)
    return app


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
