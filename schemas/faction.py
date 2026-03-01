from pydantic import BaseModel


class FactionItem(BaseModel):
    faction_id: int
    title: str

    class Config:
        from_attributes = True
