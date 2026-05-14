# views.py
from django.shortcuts import render, redirect, get_object_or_404
from admin_app.models import admin_dashboard_models
from admin_app.forms import slider_forms
from django.contrib import messages 

# INDEX / LIST
def side_slider_list(request):
    try:
        if request.user.is_superuser or request.user.role == 'central_admin' or ("campaign_management_permission" in request.user.user_permissions and (request.user.role == 'section_admin' or request.user.role == 'employee')):
            sliders = admin_dashboard_models.SideSlider.all_objects.all().order_by('-created_at')
            return render(request, 'custom-admin/side_slider/index.html', {'sliders': sliders})
        else:
            return render(request, 'permission_denied.html')
    except:
        return render(request, 'permission_denied.html')

# CREATE
def side_slider_create(request):
    try:
        if request.user.is_superuser or request.user.role == 'central_admin' or ("campaign_management_permission" in request.user.user_permissions and (request.user.role == 'section_admin' or request.user.role == 'employee')):
            form = slider_forms.SideSliderForm(request.POST or None, request.FILES or None)
            if form.is_valid():
                form.save()
                return redirect('campaign_list')

            return render(request, 'custom-admin/side_slider/create.html', {
                'form': form,
                'title': 'Add Side Slider'
            })
        else:
            return render(request, 'permission_denied.html')
    except:
        return render(request, 'permission_denied.html')


# UPDATE
def side_slider_update(request, pk):
    try:
        if request.user.is_superuser or request.user.role == 'central_admin' or ("campaign_management_permission" in request.user.user_permissions and (request.user.role == 'section_admin' or request.user.role == 'employee')):
            slider = get_object_or_404(admin_dashboard_models.SideSlider, pk=pk)
            form = slider_forms.SideSliderForm(request.POST or None, request.FILES or None, instance=slider)

            if form.is_valid():
                form.save()
                return redirect('campaign_list')

            return render(request, 'custom-admin/side_slider/update.html', {
                'form': form,
                'title': 'Edit Side Slider'
            })
        else:
            return render(request, 'permission_denied.html')
    except:
        return render(request, 'permission_denied.html')

# DELETE
def side_slider_delete(request, pk):
    try:
        if request.user.is_superuser or request.user.role == 'central_admin' or ("campaign_management_permission" in request.user.user_permissions and (request.user.role == 'section_admin' or request.user.role == 'employee')):
            slider = get_object_or_404(admin_dashboard_models.SideSlider, pk=pk)
            slider.delete()
            messages.success(request, 'Side Slider deleted successfully.')
            return redirect('campaign_list')
        else:
            messages.error(request, 'You do not have permission to delete this slider.')
            return redirect('campaign_list')
    except:
        messages.error(request, 'You do not have permission to delete this slider.')
        return redirect('campaign_list')





def slider_list(request):
    try:
        if request.user.is_superuser or request.user.role == 'central_admin' or ("slider_management_permission" in request.user.user_permissions and (request.user.role == 'section_admin' or request.user.role == 'employee')):
            sliders = admin_dashboard_models.Slider.objects.all().order_by('-created_at')
            return render(request, 'custom-admin/slider/index.html', {'sliders': sliders})
        else:
            return render(request, 'permission_denied.html')
    except:
        return render(request, 'permission_denied.html')

def slider_create(request):
    try:
        if request.user.is_superuser or request.user.role == 'central_admin' or ("slider_management_permission" in request.user.user_permissions and (request.user.role == 'section_admin' or request.user.role == 'employee')):
            if request.method == "POST":
                form = slider_forms.SliderForm(request.POST, request.FILES)
                if form.is_valid():
                    form.save()
                    return redirect('slider_list')
            else:
                form = slider_forms.SliderForm()

            return render(request, 'custom-admin/slider/create.html', {
                'form': form,
                'title': 'Create Slider'
            })
        else:
            return render(request, 'permission_denied.html')
    except:
        return render(request, 'permission_denied.html')

def slider_update(request, pk):
    try:
        if request.user.is_superuser or request.user.role == 'central_admin' or ("slider_management_permission" in request.user.user_permissions and (request.user.role == 'section_admin' or request.user.role == 'employee')):
            slider = get_object_or_404(admin_dashboard_models.Slider, pk=pk)

            if request.method == "POST":
                form = slider_forms.SliderForm(request.POST, request.FILES, instance=slider)
                if form.is_valid():
                    form.save()
                    return redirect('slider_list')
            else:
                form = slider_forms.SliderForm(instance=slider)

            return render(request, 'custom-admin/slider/update.html', {
                'form': form,
                'title': 'Update Slider'
            })
        else:
            return render(request, 'permission_denied.html')
    except:
        return render(request, 'permission_denied.html')

def slider_delete(request, pk):
    try:
        if request.user.is_superuser or request.user.role == 'central_admin' or ("slider_management_permission" in request.user.user_permissions and (request.user.role == 'section_admin' or request.user.role == 'employee')):
            slider = get_object_or_404(admin_dashboard_models.Slider, pk=pk)
            slider.delete()
            return redirect('slider_list')
        else:
            return render(request, 'permission_denied.html')
    except:
        return render(request, 'permission_denied.html')