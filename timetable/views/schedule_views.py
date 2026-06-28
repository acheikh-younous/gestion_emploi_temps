from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from timetable.forms import CourseScheduleForm
from timetable.services.permission_service import (
    is_admin,
    user_can_manage_course,
)
from timetable.models import (
    AcademicWeek,
    CourseSchedule,
    Department,
    Level,
    Section,
    TimeSlot,
)


def get_selected_week(request):
    week_id = request.GET.get("week")

    if week_id:
        week = AcademicWeek.objects.filter(id=week_id).first()
        if week:
            return week

    week = AcademicWeek.objects.filter(is_active=True).order_by("-start_date").first()

    if not week:
        week = AcademicWeek.objects.order_by("-start_date").first()

    return week


@login_required
def timetable_list(request):
    selected_week = get_selected_week(request)

    department_id = request.GET.get("department")
    section_id = request.GET.get("section")
    level_id = request.GET.get("level")

    schedules = CourseSchedule.objects.select_related(
        "week",
        "subject",
        "subject__level",
        "subject__level__section",
        "subject__level__section__department",
        "teacher",
        "room",
        "time_slot",
    )

    if selected_week:
        schedules = schedules.filter(week=selected_week)

    if department_id:
        schedules = schedules.filter(
            subject__level__section__department_id=department_id
        )

    if section_id:
        schedules = schedules.filter(
            subject__level__section_id=section_id
        )

    if level_id:
        schedules = schedules.filter(
            subject__level_id=level_id
        )

    schedules = schedules.order_by(
        "subject__level__section__department__name",
        "subject__level__section__name",
        "subject__level__name",
        "day",
        "time_slot__start_time",
    )

    departments = Department.objects.all().order_by("name")
    sections = Section.objects.select_related("department").order_by(
        "department__name",
        "name",
    )
    levels = Level.objects.select_related(
        "section",
        "section__department",
    ).order_by(
        "section__department__name",
        "section__name",
        "name",
    )
    weeks = AcademicWeek.objects.select_related("academic_year").order_by(
        "-start_date"
    )

    return render(
        request,
        "timetable/timetable_list.html",
        {
            "schedules": schedules,
            "weeks": weeks,
            "departments": departments,
            "sections": sections,
            "levels": levels,
            "selected_week": selected_week,
            "selected_department_id": department_id or "",
            "selected_section_id": section_id or "",
            "selected_level_id": level_id or "",
        },
    )


@login_required
def course_create(request):
    if request.method == "POST":
        form = CourseScheduleForm(request.POST, user=request.user)

        if form.is_valid():
            course = form.save(commit=False)
            course.created_by = request.user
            course.save()

            messages.success(request, "Cours ajouté avec succès.")
            return redirect("timetable:timetable_grid")
    else:
        form = CourseScheduleForm(user=request.user)

    return render(request, "timetable/course_form.html", {"form": form})


@login_required
def course_update(request, pk):
    course = get_object_or_404(
        CourseSchedule.objects.select_related(
            "week",
            "subject",
            "subject__level",
            "subject__level__section",
        ),
        pk=pk,
    )

    if not user_can_manage_course(request.user, course):
        messages.error(request, "Accès refusé.")
        return redirect("timetable:timetable_grid")

    if course.week.is_locked:
        messages.error(request, "Cette semaine est verrouillée.")
        return redirect("timetable:timetable_grid")

    if request.method == "POST":
        form = CourseScheduleForm(request.POST, instance=course, user=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, "Cours modifié avec succès.")
            return redirect("timetable:timetable_grid")
    else:
        form = CourseScheduleForm(instance=course, user=request.user)

    return render(request, "timetable/course_form.html", {"form": form})


@login_required
def course_delete(request, pk):
    course = get_object_or_404(
        CourseSchedule.objects.select_related(
            "week",
            "subject",
            "subject__level",
            "subject__level__section",
        ),
        pk=pk,
    )

    if not user_can_manage_course(request.user, course):
        messages.error(request, "Accès refusé.")
        return redirect("timetable:timetable_grid")

    if course.week.is_locked:
        messages.error(request, "Cette semaine est verrouillée.")
        return redirect("timetable:timetable_grid")

    if request.method == "POST":
        course.delete()
        messages.success(request, "Cours supprimé.")
        return redirect("timetable:timetable_grid")

    return render(request, "timetable/confirm_delete.html", {"object": course})


@login_required
def timetable_grid(request):
    days = [
        "LUNDI",
        "MARDI",
        "MERCREDI",
        "JEUDI",
        "VENDREDI",
        "SAMEDI",
    ]

    selected_week = get_selected_week(request)
    weeks = AcademicWeek.objects.select_related("academic_year").order_by("-start_date")
    work_slots = TimeSlot.objects.all().order_by("start_time")

    department_id = request.GET.get("department")
    section_id = request.GET.get("section")
    level_id = request.GET.get("level")

    schedules = CourseSchedule.objects.select_related(
        "week",
        "subject",
        "subject__level",
        "subject__level__section",
        "subject__level__section__department",
        "teacher",
        "room",
        "time_slot",
    )

    if selected_week:
        schedules = schedules.filter(week=selected_week)

    if department_id:
        schedules = schedules.filter(
            subject__level__section__department_id=department_id
        )

    if section_id:
        schedules = schedules.filter(
            subject__level__section_id=section_id
        )

    if level_id:
        schedules = schedules.filter(
            subject__level_id=level_id
        )

    departments = Department.objects.all().order_by("name")
    sections = Section.objects.select_related("department").order_by(
        "department__name",
        "name",
    )
    levels = Level.objects.select_related(
        "section",
        "section__department",
    ).order_by(
        "section__department__name",
        "section__name",
        "name",
    )

    timetable = {}

    for slot in work_slots:
        row = []

        for day in days:
            course = schedules.filter(
                day=day,
                time_slot=slot,
            ).first()

            row.append(
                {
                    "day": day,
                    "slot": slot,
                    "course": course,
                }
            )

        timetable[slot] = row

    return render(
        request,
        "timetable/timetable_grid.html",
        {
            "days": days,
            "timetable": timetable,
            "weeks": weeks,
            "selected_week": selected_week,
            "departments": departments,
            "sections": sections,
            "levels": levels,
            "selected_department_id": department_id or "",
            "selected_section_id": section_id or "",
            "selected_level_id": level_id or "",
        },
    )