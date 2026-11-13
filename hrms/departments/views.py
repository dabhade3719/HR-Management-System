from django.shortcuts import render, redirect
from .models import Department


def department_list(request):

    search = request.GET.get('search', '')

    departments = Department.objects.filter(
        name__icontains=search
    )

    return render(
        request,
        'departments/department_list.html',
        {
            'departments': departments,
            'search': search
        }
    )


def department_create(request):

    if request.method == 'POST':

        name = request.POST.get('name')
        description = request.POST.get('description')

        Department.objects.create(
            name=name,
            description=description
        )

        return redirect('department_list')

    return render(
        request,
        'departments/department_form.html'
    )

def department_update(request, id):

    department = Department.objects.get(id=id)

    if request.method == 'POST':

        department.name = request.POST.get('name')
        department.description = request.POST.get('description')

        department.save()

        return redirect('department_list')

    return render(
        request,
        'departments/department_form.html',
        {
            'department': department
        }
    )


def department_delete(request, id):

    department = Department.objects.get(id=id)

    if request.method == 'POST':

        department.delete()

        return redirect('department_list')

    return render(
        request,
        'departments/department_confirm_delete.html',
        {
            'department': department
        }
    )