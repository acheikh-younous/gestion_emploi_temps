from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render

from timetable.forms import LevelForm
from timetable.models import Level
from timetable.services.permission_service import is_admin


@login_required
def level_list(request):
    levels = Level.objects.select_related("section", "section__department").order_by(
        "section__department__name", "section__name", "name"
    )
    return render(request, "timetable/level_list.html", {"levels": levels})


@login_required
@user_passes_test(is_admin)
def level_create(request):
    form = LevelForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Niveau ajouté avec succès.")
        return redirect("timetable:level_list")

    return render(request, "timetable/level_form.html", {"form": form})


@login_required
@user_passes_test(is_admin)
def level_update(request, pk):
    level = get_object_or_404(Level, pk=pk)
    form = LevelForm(request.POST or None, instance=level)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Niveau modifié.")
        return redirect("timetable:level_list")

    return render(request, "timetable/level_form.html", {"form": form})


@login_required
@user_passes_test(is_admin)
def level_delete(request, pk):
    level = get_object_or_404(Level, pk=pk)

    if request.method == "POST":
        level.delete()
        messages.success(request, "Niveau supprimé.")
        return redirect("timetable:level_list")

    return render(request, "timetable/confirm_delete.html", {"object": level})