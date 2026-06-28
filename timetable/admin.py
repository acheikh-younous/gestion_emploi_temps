from django.contrib import admin

from .models import (
    AcademicYear,
    AcademicWeek,
    CourseSchedule,
    Department,
    Level,
    Room,
    Section,
    Subject,
    Teacher,
    TimeSlot,
)


@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ("name", "start_date", "end_date", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)
    ordering = ("-start_date",)


@admin.register(AcademicWeek)
class AcademicWeekAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "academic_year",
        "week_number",
        "start_date",
        "end_date",
        "is_active",
        "is_locked",
    )
    list_filter = (
        "academic_year",
        "is_active",
        "is_locked",
    )
    search_fields = (
        "academic_year__name",
    )
    ordering = ("-start_date",)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ("name", "department", "chief")
    list_filter = ("department",)
    search_fields = (
        "name",
        "department__name",
        "chief__username",
    )


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "section",
        "department",
    )

    list_filter = (
        "section__department",
        "section",
    )

    search_fields = (
        "name",
        "section__name",
    )

    @admin.display(description="Département")
    def department(self, obj):
        return obj.section.department


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = (
        "last_name",
        "first_name",
        "grade",
        "status",
        "speciality",
        "phone",
        "email",
    )

    list_filter = (
        "status",
        "grade",
    )

    search_fields = (
        "last_name",
        "first_name",
        "email",
        "phone",
    )

    ordering = (
        "last_name",
        "first_name",
    )


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "room_type",
        "capacity",
    )

    list_filter = ("room_type",)
    search_fields = ("name",)


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = (
        "start_time",
        "end_time",
    )
    ordering = ("start_time",)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
        "level",
        "section",
        "department",
        "created_by",
        "created_at",
    )

    list_filter = (
        "level__section__department",
        "level__section",
        "level",
    )

    search_fields = (
        "name",
        "code",
        "level__name",
    )

    @admin.display(description="Section")
    def section(self, obj):
        return obj.level.section

    @admin.display(description="Département")
    def department(self, obj):
        return obj.level.section.department


@admin.register(CourseSchedule)
class CourseScheduleAdmin(admin.ModelAdmin):
    list_display = (
        "subject",
        "course_type",
        "event_type",
        "teacher",
        "room",
        "week",
        "day",
        "time_slot",
        "level",
        "section",
        "created_by",
        "created_at",
    )

    list_filter = (
        "course_type",
        "event_type",
        "week",
        "day",
        "subject__level__section__department",
        "subject__level__section",
        "subject__level",
        "teacher",
        "room",
    )

    search_fields = (
        "subject__name",
        "teacher__first_name",
        "teacher__last_name",
        "room__name",
    )

    ordering = (
        "week__start_date",
        "day",
        "time_slot__start_time",
    )

    @admin.display(description="Niveau")
    def level(self, obj):
        return obj.subject.level

    @admin.display(description="Section")
    def section(self, obj):
        return obj.subject.level.section