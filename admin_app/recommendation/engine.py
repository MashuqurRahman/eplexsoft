import pandas as pd
from admin_app.models.admin_dashboard_models import (
    Product, RecentlyViewedProduct
)
from .paths import SIM_PKL


def recommend_for_user(user, limit=12):
    try:
        sim_df = pd.read_pickle(SIM_PKL)
    except FileNotFoundError:
        return Product.objects.filter(is_popular=True)[:limit]

    views = (
        RecentlyViewedProduct.objects
        .filter(user=user)
        .order_by("-view_count")[:3]  
    )

    if not views.exists():
        return Product.objects.filter(is_popular=True)[:limit]

    scores = {}

    for pid in sim_df.index:
        scores[pid] = sum(
            sim_df.at[pid, v.product_id] * v.view_count
            for v in views
            if v.product_id in sim_df
        )

    ranked_ids = sorted(scores, key=scores.get, reverse=True)

    return Product.objects.filter(id__in=ranked_ids)[:limit]