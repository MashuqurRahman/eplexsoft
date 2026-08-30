from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from pos_app.forms import inventory_forms
from pos_app.models import pos_models

@login_required
def supplier_list_view(request):
    supplier_obj = pos_models.Supplier.objects.all().order_by('-id')
    context = {
        'supplier_obj': supplier_obj
    }
    return render(request, 'pos/inventory/supplier/supplier_list.html', context)

@login_required
def supplier_index_view(request):
    supplier_obj = pos_models.Supplier.objects.all().order_by('-id')
    context = {
        'supplier_obj': supplier_obj
    }
    return render(request, 'pos/inventory/supplier/index.html', context)

@login_required
def supplier_create_view(request):
    form = inventory_forms.SupplierForm()
    if request.method == "POST":
        form = inventory_forms.SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Supplier Added Successfully!!!")
            return redirect('supplier_index_url')
        else:
            print(form.errors)
            messages.error(request, "Invalid form")

    context = {
        'form': form
    }
    return render(request, 'pos/inventory/supplier/create.html', context)

@login_required
def supplier_update_view(request, pk):
    get_obj = get_object_or_404(pos_models.Supplier, id=pk)
    form = inventory_forms.SupplierForm(instance=get_obj)
    if request.method == "POST":
        form = inventory_forms.SupplierForm(request.POST, instance=get_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Supplier Updated Successfully!!!")
            return redirect('supplier_list_url')
        else:
            print(form.errors)
            messages.error(request, "Invalid form")

    context = {
        'form': form
    }
    return render(request, 'pos/inventory/supplier/update.html', context)

@login_required
def supplier_delete_view(request, pk):
    get_obj = get_object_or_404(pos_models.Supplier, id=pk)
    get_obj.delete()
    messages.success(request, "Supplier Deleted Successfully!!!")
    return redirect('supplier_list_url')

@login_required
def pos_supplier_search_view(request):
    search_text = request.GET.get('search_text').strip()
    supplier_obj = pos_models.Supplier.objects.all().order_by('-id')
    obj_list = supplier_obj.filter(
        Q(name__icontains=search_text)|
        Q(email__icontains=search_text)|
        Q(phone__icontains=search_text)|
        Q(address__icontains=search_text)|
        Q(branch__name__icontains=search_text)
    )
    return render(request, 'pos/inventory/supplier/search.html', {'supplier_obj': obj_list})

# SUPPLIER DUE

@login_required
def supplier_due_index_view(request):
    supplier_obj = pos_models.Supplier.objects.all().order_by('-id')
    context = {
        "supplier_obj": supplier_obj
    }
    return render(request, 'pos/inventory/supplier_due/index.html', context)