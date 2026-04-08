"""Configuracao de logging da aplicacao."""

import logging


def configure_logging(log_level: str = "INFO") -> None:
    """Configura o logging padrao da aplicacao.

    Args:
        log_level: Nivel de log desejado, como ``INFO`` ou ``DEBUG``.
    """
    logging.basicConfig(
        level=getattr(logging, log_level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
