from django.contrib import messages
from django.shortcuts import render, redirect

from admin_app.forms import support_forms
from admin_app.helper import create_support_ticket,get_my_supports,get_support_details,create_support_reply


def support_create(request):

    form = support_forms.SupportForm()

    if request.method == "POST":

        form = support_forms.SupportForm(request.POST, request.FILES)

        if form.is_valid():

            response = create_support_ticket(form.cleaned_data,request)

            if response.status_code == 201:

                messages.success(
                    request,
                    "Support Ticket Submitted Successfully."
                )

                return redirect("my_supports")

            else:

                messages.error(
                    request,
                    "Failed to Submit Ticket."
                )

    return render(
        request,
        "custom-admin/support/create.html",
        {
            "form": form
        }
    )


def my_supports(request):

    response = get_my_supports(request.user.email)

    supports = []

    if response.status_code == 200:
        supports = response.json()["data"]

    return render(
        request,
        "custom-admin/support/my_supports.html",
        {
            "supports": supports
        }
    )


from django.shortcuts import render, redirect


def support_details(request, support_id):

    response = get_support_details(support_id)

    if response.status_code != 200:
        return redirect("support_list")

    ticket = response.json()

    return render(
        request,
        "custom-admin/support/support_detail.html",
        {
            "ticket": ticket
        }
    )


def support_reply(request, support_id):

    if request.method == "POST":

        data = {
            "message": request.POST.get("message")
        }

        files = {}

        if request.FILES.get("attachment"):
            files["attachment"] = request.FILES["attachment"]

        response = create_support_reply(
            support_id,
            data,
            files
        )

    return redirect("support_details", support_id=support_id)