from tortoise.models import Model
from tortoise import fields


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
