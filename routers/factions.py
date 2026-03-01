from fastapi import APIRouter
from fastapi_cache.decorator import cache
from items import FactionModel, FactionItem

router = APIRouter(prefix="/factions", tags=["factions"])


@router.get("", response_model=list[FactionItem])
@cache(expire=300)
async def get_factions():
    return await FactionModel.all()
