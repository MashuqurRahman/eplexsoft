from django.shortcuts import render, redirect
from django.contrib import messages
from ..forms import client_forms
from admin_app.models import admin_dashboard_models

def theme_setting_view(request):
    try:
        if request.user.is_superuser or request.user.role == 'central_admin' or ("theme_change_permission" in request.user.user_permissions and (request.user.role == 'section_admin' or request.user.role == 'employee')):   
            theme = admin_dashboard_models.ClientThemeSetting.objects.first()
            
            if request.method == "POST":
                form = client_forms.ThemeSettingsForm(request.POST, instance=theme)
                if form.is_valid():
                    form.save()
                    return redirect("theme_setting_url")
            else:
                form = client_forms.ThemeSettingsForm(instance=theme)
            
            context = {
                'form': form,
                'theme': theme
            }
            return render(request, 'custom-admin/theme/client_theme_setting.html', context)
        else:
            return render(request, 'permission_denied.html')
    except:
        return render(request, 'permission_denied.html')