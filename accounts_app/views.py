import email
from pyexpat.errors import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from requests.compat import urlencode
from .models import User

from client_app.views.main_menu_views import get_home_page_context

# def user_authentication_view(request):
#     errors = {}
#     context = {}
    
#     current_url = request.POST.get("current_url", "/")
#     next_url = request.POST.get("next") 

#     if request.method == "POST":
#         form_type = request.POST.get("form_type")

#         if form_type == "login":
#             email = request.POST.get("email", "").strip()
#             password = request.POST.get("password", "").strip()
#             context['email'] = email

#             if not User.objects.filter(email=email).exists():
#                 errors["email"] = "Account with this Email address does not exist"
#             else:
#                 user = authenticate(request, email=email, password=password)
#                 if user is not None:
#                     login(request, user)
#                     query_params = urlencode({"login_success": "1"})
#                     if next_url:
#                         return redirect(next_url)
#                     return redirect(f"{current_url}?{query_params}")
#                 else:
#                     errors["password"] = "Password did not match"

#             if errors:
#                 home_context = get_home_page_context(request)
#                 home_context.update({
#                     "login_errors": errors,
#                     "open_login_modal": True,
#                     "email": email,
#                     "next": next_url
#                 })
#                 return render(request, "client/home.html", home_context)

#         elif form_type == "register":
#             email = request.POST.get("email", "").strip()
#             password = request.POST.get("password")
#             confirm_password = request.POST.get("confirm_password")
#             context["email"] = email

#             if User.objects.filter(email=email).exists():
#                 errors["email"] = "Email already exists"
                
#             if password != confirm_password:
#                 errors["confirm_password"] = "Password does not match"

#             if errors:
#                 home_context = get_home_page_context(request)
#                 home_context.update({
#                     "errors": errors,
#                     "open_register_modal": True,
#                     "email": email
#                 })
#                 return render(request, "client/home.html", home_context)

#             User.objects.create_user(
#                 email=email,
#                 password=password,
#                 role="customer"
#             )

#             query_params = urlencode({"open_login_modal": 1, "email": email})
#             redirect_url = f"{current_url}?{query_params}"
#             return redirect(redirect_url)

#     home_context = get_home_page_context(request)
#     return render(request, "client/home.html", home_context)

def user_authentication_view(request):
    errors = {}
    context = {}
    
    current_url = request.POST.get("current_url", "/")
    next_url = request.POST.get("next")

    if request.method == "POST":
        form_type = request.POST.get("form_type")

        if form_type == "login":
            email = request.POST.get("email", "").strip()
            password = request.POST.get("password", "").strip()

            if not User.objects.filter(email=email).exists():
                errors["email"] = "Account with this Email address does not exist"
            else:
                user = authenticate(request, email=email, password=password)
                if user is not None:
                    login(request, user)
                    if next_url:
                        return redirect(next_url)
                    return redirect(f"{current_url}?login_success=1")
                else:
                    errors["password"] = "Password did not match"

            if errors:
                request.session["auth_errors"] = {
                    "login_errors": errors,
                    "open_login_modal": True,
                    "email": email,
                    "next": next_url
                }
                return redirect(current_url)

        elif form_type == "register":
            email = request.POST.get("email", "").strip()
            password = request.POST.get("password")
            confirm_password = request.POST.get("confirm_password")

            if User.objects.filter(email=email).exists():
                errors["email"] = "Email already exists"
                
            if password != confirm_password:
                errors["confirm_password"] = "Password does not match"

            if errors:
                request.session["auth_errors"] = {
                    "errors": errors,
                    "open_register_modal": True,
                    "email": email
                }
                return redirect(current_url)

            User.objects.create_user(
                email=email,
                password=password,
                role="customer"
            )
            return redirect(f"{current_url}?open_login_modal=1&email={email}")

    home_context = get_home_page_context(request)
    return render(request, "client/home.html", home_context)


def user_logout_view(request):
    logout(request)
    return redirect("/?logout=1")

# Admin registration

def admin_registration_view(request):
    errors = {}
    if request.method == "POST":

        email = request.POST.get('email').strip()   
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if User.objects.filter(email=email).exists():
            errors['email'] = "Email already exists"

        if password != confirm_password:
            errors['confirm_password'] = "Password does not match"

        if errors:
            return render(request, "accounts/signup.html", {
                "errors": errors,
                "email": email,
            })

        user = User.objects.create_user(
            email = email,
            password = password,

        )
        return redirect('login_url')
    
    return render(request, "accounts/signup.html")

def admin_login_view(request):
    errors = {}
    if request.method == "POST":
        email = request.POST.get('email').strip()
        password = request.POST.get('password','').strip()
        try:
            user_obj = User.objects.get(email=email)

        except User.DoesNotExist:
            errors['email'] = "Email does not exists"
            return render(request, "accounts/login.html", {
                "errors": errors,
                "email": email,
            })

        user = authenticate(request, email=user_obj.email, password=password)
        if user is None:
            errors['password'] = "Incorrect password"
            return render(request, "accounts/login.html", {
                "errors": errors,
                "password": password,
            }) 
        
        login(request, user)

        if user.role in ["central_admin", "section_admin", "employee"] or user.is_superuser:
            return redirect('admin_dashboard_url')
        else:
            return redirect('user_dashboard_url')  

    return render(request, "accounts/login.html")

def admin_logout_view(request):
    logout(request)
    return redirect("home_page_url")