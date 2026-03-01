from tortoise.models import Model
from tortoise import fields


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
