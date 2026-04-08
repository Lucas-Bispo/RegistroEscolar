"""Agregador central de rotas da API."""

from fastapi import APIRouter

from registro_escolar.api.routers.health import router as health_router

api_router = APIRouter()
api_router.include_router(health_router)
