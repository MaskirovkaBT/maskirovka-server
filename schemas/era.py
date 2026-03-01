from pydantic import BaseModel


class EraItem(BaseModel):
    era_id: int
    title: str

    class Config:
        from_attributes = True
