import os
import sys

sys.path.insert(0, "/home/aliancebrothers/aliancebrothers.com")

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "ecommerce_project.settings"
)

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()