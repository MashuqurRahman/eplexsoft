import time
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required 
from django.contrib import messages
from admin_app.models import admin_dashboard_models
from courier import services
from admin_app.forms import slider_forms

@login_required
def courier_index_view(request):
    steadfast_list = admin_dashboard_models.Courier.objects.all().order_by("-id")
    pathao_list = admin_dashboard_models.PathaoCourier.objects.all().order_by("-id")
    redx_list = admin_dashboard_models.RedxCourier.objects.all().order_by("-id")
    context = {
        'obj_list': steadfast_list,
        'pathao_list': pathao_list,
        'redx_list': redx_list
    }
    return render(request, 'custom-admin/courier/index.html', context)

@login_required
def courier_create_view(request):
    form = slider_forms.CourierForm()
    pathao_form = slider_forms.PathaoCourierForm()
    redx_form = slider_forms.RedxCourierForm()
    if request.method == "POST":
        form_type = request.POST.get("form_type")

        if form_type == "steadfast":
            form = slider_forms.CourierForm(request.POST)

            if form.is_valid():
                form.save()
                messages.success(request, "Steadfast courier added!")
                return redirect("courier_index_url")

            else:
                print(form.errors)

        elif form_type == "pathao":
            pathao_form = slider_forms.PathaoCourierForm(request.POST)

            if pathao_form.is_valid():
                pathao_form.save()
                messages.success(request, "Pathao courier added!")
                return redirect("courier_index_url")

            else:
                print(pathao_form.errors)

        elif form_type == "redx":
            redx_form = slider_forms.RedxCourierForm(request.POST)

            if redx_form.is_valid():
                redx_form.save()
                messages.success(request, "RedX courier added!")
                return redirect("courier_index_url")

            else:
                print(redx_form.errors)

    context = {
        "form": form,
        "pathao_form": pathao_form,
        "redx_form": redx_form,
    }

    return render(request, "custom-admin/courier/create.html", context)

@login_required
def courier_update_view(request, pk):
    get_obj = admin_dashboard_models.Courier.objects.get(id=pk)
    form = slider_forms.CourierUpdateForm(instance=get_obj)
    if request.method == "POST":
        form = slider_forms.CourierUpdateForm(request.POST, instance=get_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Courier information update successfully!")
            return redirect("courier_index_url")
        else:
            print(form.errors)
        
    context = {
        'form': form
    }
    return render(request, 'custom-admin/courier/update.html', context)

@login_required
def pathao_courier_update_view(request, pk):
    get_obj = admin_dashboard_models.PathaoCourier.objects.get(id=pk)
    form = slider_forms.PathaoCourierForm(instance=get_obj)
    if request.method == "POST":
        form = slider_forms.PathaoCourierForm(request.POST, instance=get_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Courier information update successfully!")
            return redirect("courier_index_url")
        else:
            print(form.errors)
        
    context = {
        'form': form
    }
    return render(request, 'custom-admin/courier/pathao_update.html', context)

@login_required
def redx_courier_update_view(request, pk):
    get_obj = admin_dashboard_models.RedxCourier.objects.get(id=pk)
    form = slider_forms.RedxCourierForm(instance=get_obj)
    if request.method == "POST":
        form = slider_forms.RedxCourierForm(request.POST, instance=get_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Courier information update successfully!")
            return redirect("courier_index_url")
        else:
            print(form.errors)
        
    context = {
        'redx_form': form
    }
    return render(request, 'custom-admin/courier/redx_update.html', context)


@login_required
def courier_delete_view(request, pk):
    get_obj = admin_dashboard_models.Courier.objects.get(id=pk)
    get_obj.delete()
    messages.success(request, "Courier information deleted successfully!!")
    return redirect("courier_index_url")

@login_required
def pathao_courier_delete_view(request, pk):
    get_obj = admin_dashboard_models.PathaoCourier.objects.get(id=pk)
    get_obj.delete()
    messages.success(request, "Courier information deleted successfully!!")
    return redirect("courier_index_url")

@login_required
def redx_courier_delete_view(request, pk):
    get_obj = admin_dashboard_models.RedxCourier.objects.get(id=pk)
    get_obj.delete()
    messages.success(request, "Courier information deleted successfully!!")
    return redirect("courier_index_url")

@login_required
def bulk_courier_form(request):
    if request.method == "POST":
        ids = request.POST.get('ids')
        courier = request.POST.get('courier')

        id_list = ids.split(',')
        orders = admin_dashboard_models.Order.objects.filter(id__in=id_list)

        for order in orders:
            if courier == "steadfast":
                services.send_order_to_steadfast(order)
            elif courier == "pathao":
                services.send_order_to_pathao(order)
            elif courier == "redx":
                services.send_order_to_redx(order)

            
        messages.success(request, "Orders sent successfully.")
        return redirect('order_list')

    ids = request.GET.get('ids', '')
    id_list = ids.split(',')
    orders = admin_dashboard_models.Order.objects.filter(id__in=id_list)

    context = {
        'orders': orders,
        'ids': ids
    }

    return render(request, 'custom-admin/courier/bulk_courier_form.html', context)

@login_required
def refresh_consignment_status_view(request, order_id):
    order = get_object_or_404(admin_dashboard_models.Order, id=order_id)

    success, msg, _ = services.refresh_consignment_status(order)

    if success:
        messages.success(request, msg)
    else:
        messages.error(request, msg)

    return redirect(request.META.get('HTTP_REFERER', ''))