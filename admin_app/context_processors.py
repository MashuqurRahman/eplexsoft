from .models import admin_dashboard_models

def theme_colors(request):
    theme = admin_dashboard_models.ThemeSetting.objects.first()
    return {
        'PRIMARY_COLOR': theme.primary_color if theme else '#eb2e61',
        'SECONDARY_COLOR': theme.secondary_color  if theme else '#fbd5df',
    }