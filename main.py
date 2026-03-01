from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_pagination import add_pagination
from tortoise.contrib.fastapi import register_tortoise, tortoise_exception_handlers

from routers import eras_router, factions_router, units_router, meta_router
from settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    FastAPICache.init(InMemoryBackend())
    yield


app = FastAPI(
    title='Maskirovka',
    lifespan=lifespan,
    exception_handlers=tortoise_exception_handlers(),
)
add_pagination(app)

# Подключение роутеров
app.include_router(eras_router)
app.include_router(factions_router)
app.include_router(units_router)
app.include_router(meta_router)

register_tortoise(
    app,
    db_url=f"{settings.db_url}",
    modules={'models': ['items']},
    generate_schemas=False,
    add_exception_handlers=True,
)
