from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Department(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Département"
        verbose_name_plural = "Départements"

    def __str__(self):
        return self.name


class Section(models.Model):
    name = models.CharField(max_length=150)
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="sections"
    )
    chief = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="managed_section"
    )

    class Meta:
        verbose_name = "Section / Filière"
        verbose_name_plural = "Sections / Filières"
        unique_together = ("name", "department")

    def __str__(self):
        return f"{self.name} - {self.department.name}"


class Level(models.Model):
    name = models.CharField(max_length=100)
    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        related_name="levels"
    )

    class Meta:
        verbose_name = "Classe / Niveau"
        verbose_name_plural = "Classes / Niveaux"
        unique_together = ("name", "section")

    def __str__(self):
        return f"{self.name} - {self.section.name}"


class Teacher(models.Model):
    STATUS_CHOICES = [
        ("PERMANENT", "Permanent"),
        ("VACATAIRE", "Vacataire"),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    grade = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PERMANENT"
    )
    speciality = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        verbose_name = "Enseignant"
        verbose_name_plural = "Enseignants"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Subject(models.Model):
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=30, blank=True, null=True)
    level = models.ForeignKey(
        Level,
        on_delete=models.CASCADE,
        related_name="subjects"
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_subjects"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Matière"
        verbose_name_plural = "Matières"
        unique_together = ("name", "level")

    def __str__(self):
        return f"{self.name} - {self.level.name}"


class Room(models.Model):
    ROOM_TYPES = [
        ("CM", "Salle de cours"),
        ("TD", "Salle TD"),
        ("TP", "Salle TP / Laboratoire"),
    ]

    name = models.CharField(max_length=100, unique=True)
    capacity = models.PositiveIntegerField(default=0)
    room_type = models.CharField(
        max_length=10,
        choices=ROOM_TYPES,
        default="CM"
    )

    class Meta:
        verbose_name = "Salle"
        verbose_name_plural = "Salles"

    def __str__(self):
        return self.name


class TimeSlot(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        verbose_name = "Créneau horaire"
        verbose_name_plural = "Créneaux horaires"
        unique_together = ("start_time", "end_time")
        ordering = ["start_time"]

    def __str__(self):
        return f"{self.start_time.strftime('%Hh%M')} - {self.end_time.strftime('%Hh%M')}"


class AcademicYear(models.Model):
    name = models.CharField(max_length=20, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Année académique"
        verbose_name_plural = "Années académiques"
        ordering = ["-start_date"]

    def __str__(self):
        return self.name


class AcademicWeek(models.Model):
    academic_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.CASCADE,
        related_name="weeks"
    )
    week_number = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Semaine académique"
        verbose_name_plural = "Semaines académiques"
        ordering = ["-start_date"]
        unique_together = ("academic_year", "week_number")

    @property
    def title(self):
        return f"Semaine {self.week_number}"

    def __str__(self):
        return f"{self.title} - {self.academic_year.name}"


class CourseSchedule(models.Model):
    DAYS = [
        ("LUNDI", "Lundi"),
        ("MARDI", "Mardi"),
        ("MERCREDI", "Mercredi"),
        ("JEUDI", "Jeudi"),
        ("VENDREDI", "Vendredi"),
        ("SAMEDI", "Samedi"),
    ]

    COURSE_TYPES = [
        ("CM", "Cours magistral"),
        ("TD", "Travaux dirigés"),
        ("TP", "Travaux pratiques"),
    ]

    EVENT_TYPES = [
        ("CT", "Cours Théorique"),
        ("CC", "Contrôle Continu"),
        ("ET", "Examen Terminal"),
        ("ER", "Examen de Rattrapage"),
        ("SEMINAIRE", "Séminaire"),
        ("SOUTENANCE", "Soutenance"),
        ("CONFERENCE", "Conférence"),
    ]

    week = models.ForeignKey(
        AcademicWeek,
        on_delete=models.CASCADE,
        related_name="schedules"
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="schedules"
    )
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name="schedules"
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="schedules"
    )
    day = models.CharField(max_length=20, choices=DAYS)
    time_slot = models.ForeignKey(
        TimeSlot,
        on_delete=models.CASCADE,
        related_name="schedules"
    )
    course_type = models.CharField(
        max_length=10,
        choices=COURSE_TYPES,
        default="CM"
    )
    event_type = models.CharField(
        max_length=30,
        choices=EVENT_TYPES,
        default="CT"
    )
    remark = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_schedules"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Cours programmé"
        verbose_name_plural = "Cours programmés"
        ordering = ["week__start_date", "day", "time_slot__start_time"]

    @property
    def level(self):
        return self.subject.level

    @property
    def section(self):
        return self.subject.level.section

    def clean(self):
        errors = {}

        if self.week and self.week.is_locked:
            errors["week"] = "Cette semaine est verrouillée. Elle ne peut plus être modifiée."

        if self.week and self.teacher and self.day and self.time_slot:
            if CourseSchedule.objects.filter(
                week=self.week,
                teacher=self.teacher,
                day=self.day,
                time_slot=self.time_slot
            ).exclude(pk=self.pk).exists():
                errors["teacher"] = "Cet enseignant a déjà un cours à ce créneau."

        if self.week and self.subject and self.day and self.time_slot:
            if CourseSchedule.objects.filter(
                week=self.week,
                subject__level=self.subject.level,
                day=self.day,
                time_slot=self.time_slot
            ).exclude(pk=self.pk).exists():
                errors["subject"] = "Cette classe a déjà un cours à ce créneau."

        if self.week and self.room and self.day and self.time_slot:
            if CourseSchedule.objects.filter(
                week=self.week,
                room=self.room,
                day=self.day,
                time_slot=self.time_slot
            ).exclude(pk=self.pk).exists():
                errors["room"] = "Cette salle est déjà utilisée à ce créneau."

        if self.course_type == "TP" and self.room and self.room.room_type != "TP":
            errors["room"] = "Pour un TP, il faut choisir une salle TP / laboratoire."

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.subject.name} - {self.day} - {self.time_slot}"