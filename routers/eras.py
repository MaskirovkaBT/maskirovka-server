from fastapi import APIRouter
from fastapi_cache.decorator import cache
from items import EraModel, EraItem

router = APIRouter(prefix="/eras", tags=["eras"])


@router.get("", response_model=list[EraItem])
@cache(expire=300)
async def get_eras():
    return await EraModel.all()
