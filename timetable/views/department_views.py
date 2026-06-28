from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render

from timetable.forms import DepartmentForm
from timetable.models import Department
from timetable.services.permission_service import is_admin


@login_required
def department_list(request):
    departments = Department.objects.all().order_by("name")
    return render(request, "timetable/department_list.html", {"departments": departments})


@login_required
@user_passes_test(is_admin)
def department_create(request):
    form = DepartmentForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Département ajouté avec succès.")
        return redirect("timetable:department_list")

    return render(request, "timetable/department_form.html", {"form": form})


@login_required
@user_passes_test(is_admin)
def department_update(request, pk):
    department = get_object_or_404(Department, pk=pk)
    form = DepartmentForm(request.POST or None, instance=department)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Département modifié.")
        return redirect("timetable:department_list")

    return render(request, "timetable/department_form.html", {"form": form})


@login_required
@user_passes_test(is_admin)
def department_delete(request, pk):
    department = get_object_or_404(Department, pk=pk)

    if request.method == "POST":
        department.delete()
        messages.success(request, "Département supprimé.")
        return redirect("timetable:department_list")

    return render(request, "timetable/confirm_delete.html", {"object": department})