from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render

from timetable.forms import TeacherForm
from timetable.models import Teacher
from timetable.services.permission_service import is_admin


@login_required
def teacher_list(request):
    teachers = Teacher.objects.all().order_by("last_name", "first_name")
    return render(request, "timetable/teacher_list.html", {"teachers": teachers})


@login_required
@user_passes_test(is_admin)
def teacher_create(request):
    form = TeacherForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Enseignant ajouté avec succès.")
        return redirect("timetable:teacher_list")

    return render(request, "timetable/teacher_form.html", {"form": form})


@login_required
@user_passes_test(is_admin)
def teacher_update(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    form = TeacherForm(request.POST or None, instance=teacher)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Enseignant modifié.")
        return redirect("timetable:teacher_list")

    return render(request, "timetable/teacher_form.html", {"form": form})


@login_required
@user_passes_test(is_admin)
def teacher_delete(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)

    if request.method == "POST":
        teacher.delete()
        messages.success(request, "Enseignant supprimé.")
        return redirect("timetable:teacher_list")

    return render(request, "timetable/confirm_delete.html", {"object": teacher})