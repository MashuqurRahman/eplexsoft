import os
from django.conf import settings

SIM_PKL = os.path.join(settings.BASE_DIR, "product_similarity.pkl")
SIM_CSV = os.path.join(settings.BASE_DIR, "product_similarity.csv")