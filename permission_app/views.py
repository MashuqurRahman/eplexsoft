from django.shortcuts import render, redirect, get_object_or_404
from collections import defaultdict
from django.db.models import Q
from django.urls import reverse
from .models import AdminPanelPermissions, PosPanelPermissions
from .forms import AdminPanelPermissionForm
from .choices import POS_PERMISSION_CHOICES, PERMISSION_GROUPS
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts_app.models import User
from pos_app.models import pos_models

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


# POS PERMISSION

PERMISSION_LABELS = dict((key, label) for key, label in POS_PERMISSION_CHOICES if key)

def build_permission_group(granted_permissions):
    groups = []
    for group_name, keys in PERMISSION_GROUPS:
        groups.append({
            'name': group_name,
            'items': [
                {
                    'key': key,
                    'label': PERMISSION_LABELS.get(key, key),
                    'granted': key in granted_permissions
                }
                for key in keys
            ],
        })
    return groups

@login_required
def pos_user_permission_view(request):
    query = request.GET.get('q', '').strip()
    branch_id = request.GET.get('branch', '').strip()
    selected_user_id = request.GET.get('user', '').strip()

    user_obj = User.objects.filter(pos_role__isnull=False).exclude(pos_role='').select_related('pos_branch')

    if query:
        user_obj = user_obj.filter(
            Q(name__icontains=query)|Q(email__icontains=query)|Q(phone__icontains=query)
        )

    if branch_id:
        user_obj = user_obj.filter(pos_branch_id=branch_id)

    user_obj = user_obj.order_by('name')

    selected_user = None
    if selected_user_id:
        selected_user = user_obj.filter(id=selected_user_id).first()
    if not selected_user:
        selected_user = user_obj.first()

    granted_permission = set()
    if selected_user:
        granted_permission = set(
            PosPanelPermissions.objects.filter(user=selected_user).values_list('permission', flat=True)
        )

    context = {
        "user_list": user_obj,
        "branches": pos_models.BrachName.objects.all().order_by("name"),
        "selected_user": selected_user,
        "permission_groups": build_permission_group(granted_permission),
        "granted_count": len(granted_permission),
        "total_permission_count": len(PERMISSION_LABELS),
        "search_query": query,
        "selected_branch": branch_id,
    }
    return render(request, 'pos/master_setup/permission/permission.html', context)

@login_required
def save_pos_permission(request, user_id):
    if request.method != "POST":
        return redirect("pos_user_permission_url")

    target_user = get_object_or_404(User, id=user_id)

    submitted = set(request.POST.getlist("permissions")) & set(PERMISSION_LABELS.keys())
    existing = set(
        PosPanelPermissions.objects.filter(user=target_user).values_list("permission", flat=True)
    )

    to_add = submitted - existing
    to_remove = existing - submitted

    PosPanelPermissions.objects.bulk_create(
        [PosPanelPermissions(user=target_user, permission=perm) for perm in to_add]
    )
    if to_remove:
        PosPanelPermissions.objects.filter(user=target_user, permission__in=to_remove).delete()

    messages.success(request, f"Permissions updated for {target_user.name or target_user.email}.")

    base_url = reverse("pos_user_permission_url")
    query_string = request.POST.get("query_string", "")
    redirect_url = f"{base_url}?user={target_user.id}"
    if query_string:
        redirect_url += f"&{query_string}"
    messages.success(request, f"Permissions updated for {target_user.name or target_user.email}.")
    return redirect(redirect_url)