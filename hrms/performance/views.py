
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Q

from .models import PerformanceReview
from .forms import PerformanceReviewForm


def has_review_permission(user):
    if not user.is_authenticated:
        return False

    if user.is_superuser:
        return True

    try:
        return user.profile.role in ['ADMIN', 'HR', 'MANAGER']
    except (AttributeError, Exception):
        return False




@login_required
def performance_list(request):
    if has_review_permission(request.user):
        reviews = PerformanceReview.objects.select_related(
            'employee', 'reviewer'
        ).all()
    else:
        try:
            employee = request.user.employee
        except Exception:
            employee = None

        if employee is None:
            reviews = PerformanceReview.objects.none()
        else:
            reviews = PerformanceReview.objects.filter(
                employee=employee
            ).select_related('employee', 'reviewer')

    # Search by employee name or employee ID
    search_query = request.GET.get('q', '').strip()

    if search_query:
        reviews = reviews.filter(
            Q(employee__first_name__icontains=search_query)
            | Q(employee__last_name__icontains=search_query)
            | Q(employee__employee_id__icontains=search_query)
        )

    # Filter by rating
    rating = request.GET.get('rating', '').strip()

    if rating in ['1', '2', '3', '4', '5']:
        reviews = reviews.filter(rating=int(rating))

    # Pagination: 10 reviews per page
    paginator = Paginator(reviews, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'performance/performance_list.html',
        {
            'reviews': page_obj,
            'page_obj': page_obj,
            'search_query': search_query,
            'selected_rating': rating,
        }
    )

@login_required
def performance_create(request):
    if not has_review_permission(request.user):
        raise PermissionDenied(
            'You are not allowed to create performance reviews.'
        )

    if request.method == 'POST':
        form = PerformanceReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user
            review.save()

            messages.success(
                request,
                'Performance review created successfully.'
            )
            return redirect('performance_list')
    else:
        form = PerformanceReviewForm()

    return render(
        request,
        'performance/performance_form.html',
        {'form': form}
    )


@login_required
def performance_detail(request, pk):
    review = get_object_or_404(
        PerformanceReview.objects.select_related('employee', 'reviewer'),
        pk=pk
    )

    is_reviewer_role = has_review_permission(request.user)

    if not is_reviewer_role:
        try:
            is_own_review = review.employee.user_id == request.user.id
        except Exception:
            is_own_review = False

        if not is_own_review:
            raise PermissionDenied(
                'You are not allowed to view this review.'
            )

    return render(
        request,
        'performance/performance_detail.html',
        {'review': review}
    )