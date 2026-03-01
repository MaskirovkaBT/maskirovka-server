from fastapi import APIRouter
from fastapi_cache.decorator import cache
from models import FactionModel
from schemas import FactionItem

router = APIRouter(prefix="/factions", tags=["factions"])


@router.get("", response_model=list[FactionItem])
@cache(expire=300)
async def get_factions():
    return await FactionModel.all().order_by('title')
