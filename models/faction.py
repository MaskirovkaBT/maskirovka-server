from tortoise.models import Model
from tortoise import fields


class FactionModel(Model):
    faction_id = fields.IntField(primary_key=True)
    title = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = 'faction_items'
