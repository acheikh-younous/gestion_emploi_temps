from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from timetable.forms import SubjectForm
from timetable.models import Subject
from timetable.services.permission_service import user_can_manage_subject


@login_required
def subject_list(request):
    subjects = Subject.objects.select_related(
        "level", "level__section", "level__section__department"
    ).order_by(
        "level__section__department__name",
        "level__section__name",
        "level__name",
        "name",
    )

    return render(request, "timetable/subject_list.html", {"subjects": subjects})


@login_required
def subject_create(request):
    form = SubjectForm(request.POST or None, user=request.user)

    if request.method == "POST" and form.is_valid():
        subject = form.save(commit=False)
        subject.created_by = request.user
        subject.save()
        messages.success(request, "Matière ajoutée.")
        return redirect("timetable:subject_list")

    return render(request, "timetable/subject_form.html", {"form": form})


@login_required
def subject_update(request, pk):
    subject = get_object_or_404(
        Subject.objects.select_related("level", "level__section"),
        pk=pk,
    )

    if not user_can_manage_subject(request.user, subject):
        messages.error(request, "Accès refusé.")
        return redirect("timetable:subject_list")

    form = SubjectForm(request.POST or None, instance=subject, user=request.user)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Matière modifiée.")
        return redirect("timetable:subject_list")

    return render(request, "timetable/subject_form.html", {"form": form})


@login_required
def subject_delete(request, pk):
    subject = get_object_or_404(
        Subject.objects.select_related("level", "level__section"),
        pk=pk,
    )

    if not user_can_manage_subject(request.user, subject):
        messages.error(request, "Accès refusé.")
        return redirect("timetable:subject_list")

    if request.method == "POST":
        subject.delete()
        messages.success(request, "Matière supprimée.")
        return redirect("timetable:subject_list")

    return render(request, "timetable/confirm_delete.html", {"object": subject})