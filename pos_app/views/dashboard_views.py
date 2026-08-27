from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def pos_dashboard_view(request):
    return render(request, 'pos/dashboard.html')