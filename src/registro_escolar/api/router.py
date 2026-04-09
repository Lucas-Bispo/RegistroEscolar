"""Agregador central de rotas da API."""

from fastapi import APIRouter

from registro_escolar.api.routers.academic_terms import router as academic_terms_router
from registro_escolar.api.routers.api_root import router as api_root_router
from registro_escolar.api.routers.classes import router as classes_router
from registro_escolar.api.routers.health import router as health_router
from registro_escolar.api.routers.schools import router as schools_router
from registro_escolar.core.config import get_settings

settings = get_settings()

api_router = APIRouter(prefix=settings.api_v1_prefix)
api_router.include_router(api_root_router)
api_router.include_router(academic_terms_router)
api_router.include_router(classes_router)
api_router.include_router(health_router)
api_router.include_router(schools_router)
