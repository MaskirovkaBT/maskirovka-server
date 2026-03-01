from tortoise.expressions import Q, RawSQL
from items import UnitModel


async def build_unit_query(
    era_id: int | None = None,
    faction_id: list[int] | None = None,
    unit_type: str | None = None,
    title: str | None = None,
    role: str | None = None,
    specials: str | None = None,
    pv: int | None = None,
    sz: int | None = None,
    short: int | None = None,
    medium: int | None = None,
    long: int | None = None,
    extreme: int | None = None,
    ov: int | None = None,
    armor: int | None = None,
    struc: int | None = None,
    threshold: int | None = None,
    mv: int | None = None,

    x_specials_mode: str = "or",
    x_pv_mode: str = "eq",
    x_sz_mode: str = "eq",
    x_short_mode: str = "eq",
    x_medium_mode: str = "eq",
    x_long_mode: str = "eq",
    x_extreme_mode: str = "eq",
    x_ov_mode: str = "eq",
    x_armor_mode: str = "eq",
    x_struc_mode: str = "eq",
    x_threshold_mode: str = "eq",
    x_mv_mode: str = "eq",
    sort_by: str | None = None,
    sort_order: str = "asc",
):
    query = UnitModel.all()

    if era_id:
        query = query.filter(unit_items__era=era_id)

    if faction_id:
        query = query.filter(unit_items__faction_id__in=faction_id)

    if unit_type:
        query = query.filter(unit_type__icontains=unit_type)

    if title:
        query = query.filter(title__icontains=title)

    if role:
        query = query.filter(role__icontains=role)

    if specials:
        specials_list = [s.strip() for s in specials.split(',')]
        specials_filter = Q()
        for s in specials_list:
            if x_specials_mode == 'or':
                specials_filter |= Q(specials__icontains=s)
            else:
                specials_filter &= Q(specials__icontains=s)
        query = query.filter(specials_filter)

    operators = {
        "eq": "",
        "gt": "__gt",
        "gte": "__gte",
        "lt": "__lt",
        "lte": "__lte",
    }

    if pv:
        suffix = operators.get(x_pv_mode, "")
        query = query.filter(**{f"pv{suffix}": pv})

    if sz:
        suffix = operators.get(x_sz_mode, "")
        query = query.filter(**{f"sz{suffix}": sz})

    if short:
        suffix = operators.get(x_short_mode, "")
        query = query.filter(**{f"short{suffix}": short})

    if medium:
        suffix = operators.get(x_medium_mode, "")
        query = query.filter(**{f"medium{suffix}": medium})

    if long:
        suffix = operators.get(x_long_mode, "")
        query = query.filter(**{f"long{suffix}": long})

    if extreme:
        suffix = operators.get(x_extreme_mode, "")
        query = query.filter(**{f"extreme{suffix}": extreme})

    if ov:
        suffix = operators.get(x_ov_mode, "")
        query = query.filter(**{f"ov{suffix}": ov})

    if armor:
        suffix = operators.get(x_armor_mode, "")
        query = query.filter(**{f"armor{suffix}": armor})

    if struc:
        suffix = operators.get(x_struc_mode, "")
        query = query.filter(**{f"struc{suffix}": struc})

    if threshold:
        suffix = operators.get(x_threshold_mode, "")
        query = query.filter(**{f"threshold{suffix}": threshold})

    if mv:
        suffix = operators.get(x_mv_mode, "")
        filter_key = f"mv_int{suffix}"
        query = query.annotate(
            mv_int=RawSQL("CAST(mv AS INTEGER)")
        ).filter(**{filter_key: mv})

    valid_sort_fields = {"title", "pv", "role", "short", "medium", "long", "armor", "struc", "mv"}
    if sort_by and sort_by in valid_sort_fields:
        if sort_by == "mv":
            query = query.annotate(
                mv_int=RawSQL("CAST(mv AS INTEGER)")
            )
            order_prefix = "-" if sort_order.lower() == "desc" else ""
            query = query.order_by(f"{order_prefix}mv_int")
        else:
            order_prefix = "-" if sort_order.lower() == "desc" else ""
            query = query.order_by(f"{order_prefix}{sort_by}")

    return query
