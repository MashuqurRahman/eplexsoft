from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from admin_app.models import admin_dashboard_models
from ..forms import client_forms


def contact_page_view(request):
    form = client_forms.ContactForm()
    if request.method == "POST":
        form = client_forms.ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Message Sent Successfully!!!")
        else:
            messages.error(request, "Invalid form.")

    context = {
        'form': form
    }
    return render(request, 'client/contact/contact.html', context)

def client_about_us_view(request):
    obj_list = admin_dashboard_models.AboutUs.objects.first()
    return render(request, 'client/footer/about_us.html', {'object': obj_list})

def client_terms_and_conditions_view(request):
    obj_list = admin_dashboard_models.TermsCondition.objects.filter(head='terms_and_conditions', is_active=True)
    return render(request, 'client/footer/terms_condition.html', {'obj_list': obj_list})

def client_privecy_and_policy_view(request):
    obj_list = admin_dashboard_models.TermsCondition.objects.filter(head='privacy_and_policy', is_active=True)
    return render(request, 'client/footer/privecy_policy.html', {'obj_list': obj_list})

def client_return_and_refund_view(request):
    obj_list = admin_dashboard_models.TermsCondition.objects.filter(head='return_refund', is_active=True)
    return render(request, 'client/footer/return_refund.html', {'obj_list': obj_list})

def client_warranty_policy_view(request):
    obj_list = admin_dashboard_models.TermsCondition.objects.filter(head='warranty', is_active=True)
    return render(request, 'client/footer/warranty_policy.html', {'obj_list': obj_list})

def client_emi_policy_view(request):
    obj_list = admin_dashboard_models.TermsCondition.objects.filter(head='emi', is_active=True)
    return render(request, 'client/footer/emi_policy.html', {'obj_list': obj_list})

