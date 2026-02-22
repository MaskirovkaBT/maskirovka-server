from tortoise.models import Model
from tortoise import fields
from pydantic import BaseModel

class EraFactionItem(Model):
    id = fields.IntField(primary_key=True)
    era = fields.ForeignKeyField(
        'models.EraModel',
        related_name='era_items'
    )
    faction = fields.ForeignKeyField(
        'models.FactionModel',
        related_name='faction_items'
    )
    unit = fields.ForeignKeyField(
        'models.UnitModel',
        related_name='unit_items'
    )
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = 'era_faction_items'

class EraModel(Model):
    era_id = fields.IntField(primary_key=True)
    title = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = 'era_items'

class EraItem(BaseModel):
    era_id: int
    title: str

    class Config:
        from_attributes = True

class FactionModel(Model):
    faction_id = fields.IntField(primary_key=True)
    title = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = 'faction_items'

class FactionItem(BaseModel):
    faction_id: int
    title: str

    class Config:
        from_attributes = True

class UnitModel(Model):
    unit_id = fields.IntField(primary_key=True)
    unit_type = fields.TextField()
    title = fields.TextField()
    pv = fields.IntField(default=0)
    role = fields.TextField()
    sz = fields.IntField(default=0)
    mv = fields.TextField()
    short = fields.IntField(default=0)
    medium = fields.IntField(default=0)
    long = fields.IntField(default=0)
    extreme = fields.IntField(default=0)
    ov = fields.IntField(default=0)
    armor = fields.IntField(default=0)
    struc = fields.IntField(default=0)
    threshold = fields.IntField(default=0)
    specials = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = 'unit_items'

class UnitItem(BaseModel):
    unit_id: int
    unit_type: str
    title: str
    pv: int
    role: str
    sz: int
    mv: str
    short: int
    medium: int
    long: int
    extreme: int
    ov: int
    armor: int
    struc: int
    threshold: int
    specials: str