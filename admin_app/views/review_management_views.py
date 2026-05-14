import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core.paginator import Page, PageNotAnInteger, EmptyPage, Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from client_app.models import client_models
from admin_app.forms import review_management_forms

@login_required
def review_list_view(request):
    reviews = client_models.ReviewRating.objects.all().order_by('-id')
    
    page = request.GET.get('page')
    paginator = Paginator(reviews, 20)

    try:
        reviews = paginator.page(page)
    except PageNotAnInteger:
        reviews = paginator.page(1)
    except EmptyPage:
        reviews = paginator.page(paginator.num_pages)

    context = {
        'reviews': reviews
    }
    return render(request, 'custom-admin/review/index.html', context)

@login_required
def delete_review_view(request, review_id):
    review = client_models.ReviewRating.objects.get(id=review_id)
    if review:
        review.delete()
        messages.success(request, 'Review deleted successfully.')
    else:
        messages.error(request, 'Review not found.')
    return redirect('review_list_url')

@login_required
def review_update_view(request, review_id):
    review = client_models.ReviewRating.objects.get(id=review_id)
    if request.method == 'POST':
        form = review_management_forms.ReviewRatingForm(request.POST, instance=review)

        if form.is_valid():
            form.save()
            messages.success(request, 'Review updated successfully.')
            return redirect('review_list_url')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = review_management_forms.ReviewRatingForm(instance=review)

    context = {
        'form': form,
        'review': review
    }
    return render(request, 'custom-admin/review/update.html', context)  

@login_required
def toggle_review_selection(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        review_id = data.get('review_id')
        is_selected = data.get('is_selected')

        review = client_models.ReviewRating.objects.get(id=review_id)
        review.is_selected = is_selected
        review.save()
        
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def review_search_view(request):
    query = request.GET.get('search_id', '')
    reviews = (
        client_models.ReviewRating.objects.filter(product__product_name__icontains=query)|
        client_models.ReviewRating.objects.filter(rating__icontains=query)|
        client_models.ReviewRating.objects.filter(review__icontains=query)|
        client_models.ReviewRating.objects.filter(user__email__icontains=query)
    ).order_by('-id')
    
    context = {
        'reviews': reviews
    }
    return render(request, 'custom-admin/review/search.html', context)
