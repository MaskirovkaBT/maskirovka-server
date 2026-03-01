from contextlib import asynccontextmanager

from fastapi import FastAPI, Query, Header, HTTPException
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache
from fastapi_pagination import Page, add_pagination
from fastapi_pagination.ext.tortoise import apaginate
from tortoise.contrib.fastapi import register_tortoise, tortoise_exception_handlers
from tortoise.expressions import Q, RawSQL

from items import *
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


@app.get('/eras', response_model=list[EraItem])
@cache(expire=300)
async def get_eras():
    return await EraModel.all()


@app.get('/factions', response_model=list[FactionItem])
@cache(expire=300)
async def get_factions():
    return await FactionModel.all()


@app.get('/units')
async def get_units(
        era_id: int | None = None,
        faction_id: list[int] | None = Query(None),
        unit_type: str | None = None,
        title: str | None = None,
        role: str | None = None,
        specials: str | None = Query(None, min_length=2),
        pv: int | None = None,
        sz: int | None = None,
        short: int | None = None,
        medium: int | None = None,
        long: int | None = None,
        extreme: int | None = None,
        ov: int | None = None,
        armor: int | None = None,
        struc: int | None = None,
        threshold: int | None = None,
        mv: int | None = None,

        x_specials_mode: str = Header("or", alias="X-Specials-Mode"),
        x_pv_mode: str = Header("eq", alias="X-Pv-Mode"),
        x_sz_mode: str = Header("eq", alias="X-Sz-Mode"),
        x_short_mode: str = Header("eq", alias="X-Short-Mode"),
        x_medium_mode: str = Header("eq", alias="X-Medium-Mode"),
        x_long_mode: str = Header("eq", alias="X-Long-Mode"),
        x_extreme_mode: str = Header("eq", alias="X-Extreme-Mode"),
        x_ov_mode: str = Header("eq", alias="X-Ov-Mode"),
        x_armor_mode: str = Header("eq", alias="X-Armor-Mode"),
        x_struc_mode: str = Header("eq", alias="X-Struc-Mode"),
        x_threshold_mode: str = Header("eq", alias="X-Threshold-Mode"),
        x_mv_mode: str = Header("eq", alias="X-Mv-Mode"),
) -> Page[UnitItem]:
    query = UnitModel.all()

    if era_id:
        query = query.filter(unit_items__era=era_id)

    if faction_id:
        query = query.filter(unit_items__faction_id__in=faction_id)

    if unit_type:
        query = query.filter(unit_type__icontains=unit_type)

    if title:
        query = query.filter(title__icontains=title)

    if role:
        query = query.filter(role__icontains=role)

    if specials:
        specials_list = [s.strip() for s in specials.split(',')]
        specials_filter = Q()
        for s in specials_list:
            if x_specials_mode == 'or':
                specials_filter |= Q(specials__icontains=s)
            else:
                specials_filter &= Q(specials__icontains=s)
        query = query.filter(specials_filter)

    operators = {
        "eq": "",
        "gt": "__gt",
        "gte": "__gte",
        "lt": "__lt",
        "lte": "__lte",
    }

    valid_modes = {"eq", "gt", "gte", "lt", "lte"}
    mode_headers = {
        "x_pv_mode": x_pv_mode,
        "x_sz_mode": x_sz_mode,
        "x_short_mode": x_short_mode,
        "x_medium_mode": x_medium_mode,
        "x_long_mode": x_long_mode,
        "x_extreme_mode": x_extreme_mode,
        "x_ov_mode": x_ov_mode,
        "x_armor_mode": x_armor_mode,
        "x_struc_mode": x_struc_mode,
        "x_threshold_mode": x_threshold_mode,
        "x_mv_mode": x_mv_mode,
    }
    for header_name, mode_value in mode_headers.items():
        if mode_value not in valid_modes:
            raise HTTPException(
                status_code=400,
                detail=f"Невалидное значение заголовка {header_name}: '{mode_value}'."
                       f"Допустимые значения: {', '.join(valid_modes)}"
            )

    if pv:
        suffix = operators.get(x_pv_mode, "")
        filter_key = f"pv{suffix}"
        query = query.filter(**{filter_key: pv})

    if sz:
        suffix = operators.get(x_sz_mode, "")
        filter_key = f"sz{suffix}"
        query = query.filter(**{filter_key: sz})

    if short:
        suffix = operators.get(x_short_mode, "")
        filter_key = f"short{suffix}"
        query = query.filter(**{filter_key: short})

    if medium:
        suffix = operators.get(x_medium_mode, "")
        filter_key = f"medium{suffix}"
        query = query.filter(**{filter_key: medium})

    if long:
        suffix = operators.get(x_long_mode, "")
        filter_key = f"long{suffix}"
        query = query.filter(**{filter_key: long})

    if extreme:
        suffix = operators.get(x_extreme_mode, "")
        filter_key = f"extreme{suffix}"
        query = query.filter(**{filter_key: extreme})

    if ov:
        suffix = operators.get(x_ov_mode, "")
        filter_key = f"ov{suffix}"
        query = query.filter(**{filter_key: ov})

    if armor:
        suffix = operators.get(x_armor_mode, "")
        filter_key = f"armor{suffix}"
        query = query.filter(**{filter_key: armor})

    if struc:
        suffix = operators.get(x_struc_mode, "")
        filter_key = f"struc{suffix}"
        query = query.filter(**{filter_key: struc})

    if threshold:
        suffix = operators.get(x_threshold_mode, "")
        filter_key = f"threshold{suffix}"
        query = query.filter(**{filter_key: threshold})

    if mv:
        suffix = operators.get(x_mv_mode, "")
        filter_key = f"mv_int{suffix}"
        query = (query.annotate(
            mv_int=RawSQL("CAST(mv AS INTEGER)")
        ).filter(**{filter_key: mv}))

    return await apaginate(query.distinct())


@app.get('/roles')
@cache(expire=300)
async def get_roles():
    return await (UnitModel
                  .all()
                  .distinct()
                  .order_by('role')
                  .values_list('role', flat=True))


@app.get('/types')
@cache(expire=300)
async def get_types():
    return await (UnitModel
                  .all()
                  .distinct()
                  .order_by('unit_type')
                  .values_list('unit_type', flat=True))


register_tortoise(
    app,
    db_url=f"{settings.db_url}",
    modules={'models': ['items']},
    generate_schemas=False,
    add_exception_handlers=True,
)
