from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from .models import (
    Department,
    Section,
    Level,
    Teacher,
    Subject,
    Room,
    TimeSlot,
    CourseSchedule
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
        fields = ["first_name", "last_name", "phone", "email"]


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ["name", "code", "course_type", "level"]


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ["name", "capacity", "room_type"]


class TimeSlotForm(forms.ModelForm):
    class Meta:
        model = TimeSlot
        fields = ["start_time", "end_time"]


class CourseScheduleForm(forms.ModelForm):
    class Meta:
        model = CourseSchedule
        fields = [
            "subject",
            "teacher",
            "level",
            "room",
            "day",
            "time_slot"
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})

        if user and not user.is_staff and not user.is_superuser:
            try:
                section = user.managed_section

                self.fields["level"].queryset = Level.objects.filter(section=section)
                self.fields["subject"].queryset = Subject.objects.filter(level__section=section)

            except Section.DoesNotExist:
                self.fields["level"].queryset = Level.objects.none()
                self.fields["subject"].queryset = Subject.objects.none()


class ChiefUserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        initial="1234",
        help_text="Mot de passe par défaut : 1234"
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.is_staff = False
        user.is_superuser = False

        if commit:
            user.save()

        return user