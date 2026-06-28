from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render

from timetable.forms import AcademicWeekForm
from timetable.models import AcademicWeek
from timetable.services.permission_service import is_admin


@login_required
def week_list(request):
    weeks = AcademicWeek.objects.select_related("academic_year").order_by("-start_date")
    return render(request, "timetable/week_list.html", {"weeks": weeks})


@login_required
@user_passes_test(is_admin)
def week_create(request):
    form = AcademicWeekForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Semaine ajoutée avec succès.")
        return redirect("timetable:week_list")

    return render(request, "timetable/week_form.html", {"form": form})


@login_required
@user_passes_test(is_admin)
def week_update(request, pk):
    week = get_object_or_404(AcademicWeek, pk=pk)
    form = AcademicWeekForm(request.POST or None, instance=week)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Semaine modifiée.")
        return redirect("timetable:week_list")

    return render(request, "timetable/week_form.html", {"form": form})


@login_required
@user_passes_test(is_admin)
def week_delete(request, pk):
    week = get_object_or_404(AcademicWeek, pk=pk)

    if request.method == "POST":
        week.delete()
        messages.success(request, "Semaine supprimée.")
        return redirect("timetable:week_list")

    return render(request, "timetable/confirm_delete.html", {"object": week})