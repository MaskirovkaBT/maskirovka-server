from fastapi import APIRouter
from fastapi_cache.decorator import cache
from models import UnitModel

router = APIRouter(tags=["meta"])


@router.get("/roles")
@cache(expire=300)
async def get_roles():
    return await (
        UnitModel
        .all()
        .distinct()
        .order_by('role')
        .values_list('role', flat=True)
    )


@router.get("/types")
@cache(expire=300)
async def get_types():
    return await (
        UnitModel
        .all()
        .distinct()
        .order_by('unit_type')
        .values_list('unit_type', flat=True)
    )
