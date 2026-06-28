from django import forms
from django.contrib.auth.models import User

from .models import (
    AcademicWeek,
    AcademicYear,
    CourseSchedule,
    Department,
    Level,
    Room,
    Section,
    Subject,
    Teacher,
)


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ["name", "description"]


class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ["name", "department", "chief"]


class LevelForm(forms.ModelForm):
    class Meta:
        model = Level
        fields = ["name", "section"]


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = [
            "first_name",
            "last_name",
            "phone",
            "email",
            "grade",
            "status",
            "speciality",
        ]


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ["name", "capacity", "room_type"]


class SubjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if user and not user.is_staff and not user.is_superuser:
            section = getattr(user, "managed_section", None)
            self.fields["level"].queryset = Level.objects.filter(
                section=section
            )

    class Meta:
        model = Subject
        fields = ["name", "code", "level"]


class AcademicYearForm(forms.ModelForm):
    class Meta:
        model = AcademicYear
        fields = ["name", "start_date", "end_date", "is_active"]

        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }


class AcademicWeekForm(forms.ModelForm):
    class Meta:
        model = AcademicWeek
        fields = [
            "academic_year",
            "week_number",
            "start_date",
            "end_date",
            "is_active",
            "is_locked",
        ]

        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }


class CourseScheduleForm(forms.ModelForm):
    program_all_day = forms.BooleanField(
        required=False,
        label="Programmer toute la journée"
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if user and not user.is_staff and not user.is_superuser:
            section = getattr(user, "managed_section", None)
            self.fields["subject"].queryset = Subject.objects.filter(
                level__section=section
            )

        self.fields["week"].label = "Semaine"
        self.fields["subject"].label = "Matière"
        self.fields["teacher"].label = "Enseignant"
        self.fields["room"].label = "Salle"
        self.fields["day"].label = "Jour"
        self.fields["time_slot"].label = "Créneau horaire"
        self.fields["course_type"].label = "Type de séance"
        self.fields["event_type"].label = "Type d'événement"
        self.fields["remark"].label = "Remarque"

    class Meta:
        model = CourseSchedule
        fields = [
            "week",
            "subject",
            "teacher",
            "room",
            "day",
            "time_slot",
            "course_type",
            "event_type",
            "remark",
        ]


class ChiefUserForm(forms.ModelForm):
    password = forms.CharField(
        initial="1234",
        widget=forms.PasswordInput,
        label="Mot de passe par défaut"
    )

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.is_staff = False
        user.is_superuser = False

        if commit:
            user.save()

        return user