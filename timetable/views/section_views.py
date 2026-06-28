from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render

from timetable.forms import SectionForm
from timetable.models import Section
from timetable.services.permission_service import is_admin


@login_required
def section_list(request):
    sections = Section.objects.select_related("department", "chief").order_by(
        "department__name", "name"
    )
    return render(request, "timetable/section_list.html", {"sections": sections})


@login_required
@user_passes_test(is_admin)
def section_create(request):
    form = SectionForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Section ajoutée avec succès.")
        return redirect("timetable:section_list")

    return render(request, "timetable/section_form.html", {"form": form})


@login_required
@user_passes_test(is_admin)
def section_update(request, pk):
    section = get_object_or_404(Section, pk=pk)
    form = SectionForm(request.POST or None, instance=section)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Section modifiée.")
        return redirect("timetable:section_list")

    return render(request, "timetable/section_form.html", {"form": form})


@login_required
@user_passes_test(is_admin)
def section_delete(request, pk):
    section = get_object_or_404(Section, pk=pk)

    if request.method == "POST":
        section.delete()
        messages.success(request, "Section supprimée.")
        return redirect("timetable:section_list")

    return render(request, "timetable/confirm_delete.html", {"object": section})