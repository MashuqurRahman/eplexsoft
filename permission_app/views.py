from django.shortcuts import render, redirect, get_object_or_404
from collections import defaultdict
from .models import AdminPanelPermissions
from .forms import AdminPanelPermissionForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def permission_list(request):
    permissions = AdminPanelPermissions.objects.select_related('user')

    if request.user.is_superuser:
        pass
    elif request.user.role == 'central_admin':
        permissions = permissions.exclude(user__role='central_admin').exclude(user__is_superuser=True)
    elif request.user.role == 'section_admin':
        if "permission_management" in request.user.user_permissions:
            permissions = permissions.filter(user__role__in = ['section_admin', 'employee'])
        else:
            return render(request, 'permission_denied.html')
    elif request.user.role == 'employee':
        if "permission_management" in request.user.user_permissions:
            permissions = permissions.filter(user__role = 'employee')
        else:
            return render(request, 'permission_denied.html')
    else:
        permissions = permissions.none()

    grouped_permissions = defaultdict(list)

    for perm in permissions:
        grouped_permissions[perm.user].append(perm)

    context = {
        'grouped_permissions': dict(grouped_permissions)
    }
    return render(request, 'custom-admin/permission/index.html', context)


@login_required
def permission_create(request):
    form = AdminPanelPermissionForm(role=request.user.role)
    if request.method == 'POST':
        form = AdminPanelPermissionForm(request.POST or None, role=request.user.role)
        if form.is_valid():
            form.save()
            messages.success(request, "Permission created successfully!")
            return redirect('permission_list')
        else:
            # This captures the ValidationError from your forms.py
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
                    
    return render(request, 'custom-admin/permission/create.html', {'form': form})



@login_required
def permission_delete(request, pk):
    try:
        permission = get_object_or_404(AdminPanelPermissions, pk=pk)
        permission.delete()
        messages.success(request, "Permission Deleted Successfully!!!")
        return redirect('permission_list')
    except:
        messages.error(request, "Delete is not possible!!")
        return redirect('permission_list')
