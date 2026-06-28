from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from timetable.models import (
    CourseSchedule,
    Department,
    Level,
    Room,
    Section,
    Subject,
    Teacher,
    AcademicWeek,
)

from timetable.services.permission_service import is_admin, get_user_section


@login_required
def dashboard(request):
    if is_admin(request.user):
        context = {
            "departments_count": Department.objects.count(),
            "sections_count": Section.objects.count(),
            "levels_count": Level.objects.count(),
            "teachers_count": Teacher.objects.count(),
            "subjects_count": Subject.objects.count(),
            "rooms_count": Room.objects.count(),
            "weeks_count": AcademicWeek.objects.count(),
            "schedules_count": CourseSchedule.objects.count(),
        }
    else:
        section = get_user_section(request.user)

        context = {
            "teachers_count": Teacher.objects.count(),
            "rooms_count": Room.objects.count(),
            "subjects_count": Subject.objects.filter(
                level__section=section
            ).count(),
            "levels_count": Level.objects.filter(
                section=section
            ).count(),
            "schedules_count": CourseSchedule.objects.filter(
                subject__level__section=section
            ).count(),
        }

    return render(request, "timetable/dashboard.html", context)