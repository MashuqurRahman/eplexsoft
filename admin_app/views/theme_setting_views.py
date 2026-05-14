from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from ..models import admin_dashboard_models
from ..forms import theme_setting_forms

@login_required
def theme_setting_view(request):
    try:
        if request.user.is_superuser or request.user.role == 'central_admin' or ("theme_change_permission" in request.user.user_permissions and (request.user.role == 'section_admin' or request.user.role == 'employee')):   
            theme = admin_dashboard_models.ThemeSetting.objects.first()
            
            if request.method == "POST":
                form = theme_setting_forms.ThemeSettingForm(request.POST, instance=theme)
                if form.is_valid():
                    form.save()
                    return redirect("theme_settings")
            else:
                form = theme_setting_forms.ThemeSettingForm(instance=theme)

            context = {
                'form': form,
                'theme': theme
            }
            return render(request, 'custom-admin/theme/theme_settings.html', context)
        else:
            return render(request, 'permission_denied.html')
    except:
        return render(request, 'permission_denied.html')