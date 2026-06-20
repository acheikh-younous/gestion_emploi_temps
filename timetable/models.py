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
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    class Meta:
        verbose_name = "Enseignant"
        verbose_name_plural = "Enseignants"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Subject(models.Model):
    COURSE_TYPES = [
        ("CM", "Cours magistral"),
        ("TD", "Travaux dirigés"),
        ("TP", "Travaux pratiques"),
    ]

    name = models.CharField(max_length=150)
    code = models.CharField(max_length=30, blank=True, null=True)
    course_type = models.CharField(max_length=10, choices=COURSE_TYPES, default="CM")
    level = models.ForeignKey(
        Level,
        on_delete=models.CASCADE,
        related_name="subjects"
    )

    class Meta:
        verbose_name = "Matière"
        verbose_name_plural = "Matières"
        unique_together = ("name", "level")

    def __str__(self):
        return f"{self.name} ({self.level.name})"


class Room(models.Model):
    ROOM_TYPES = [
        ("CM", "Salle de cours"),
        ("TD", "Salle TD"),
        ("TP", "Salle TP / Laboratoire"),
    ]

    name = models.CharField(max_length=100, unique=True)
    capacity = models.PositiveIntegerField(default=0)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPES, default="CM")

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


class CourseSchedule(models.Model):
    DAYS = [
        ("LUNDI", "Lundi"),
        ("MARDI", "Mardi"),
        ("MERCREDI", "Mercredi"),
        ("JEUDI", "Jeudi"),
        ("VENDREDI", "Vendredi"),
        ("SAMEDI", "Samedi"),
    ]

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

    level = models.ForeignKey(
        Level,
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
        ordering = ["day", "time_slot__start_time"]

    def clean(self):
        errors = {}

        # Vérifier que la matière appartient bien au niveau choisi
        if self.subject and self.level:
            if self.subject.level != self.level:
                errors["subject"] = "Cette matière n'appartient pas à cette classe / ce niveau."

        # Conflit enseignant
        teacher_conflict = CourseSchedule.objects.filter(
            teacher=self.teacher,
            day=self.day,
            time_slot=self.time_slot
        ).exclude(pk=self.pk)

        if teacher_conflict.exists():
            errors["teacher"] = "Cet enseignant a déjà un cours à ce créneau."

        # Conflit classe / niveau
        level_conflict = CourseSchedule.objects.filter(
            level=self.level,
            day=self.day,
            time_slot=self.time_slot
        ).exclude(pk=self.pk)

        if level_conflict.exists():
            errors["level"] = "Cette classe a déjà un cours à ce créneau."

        # Conflit salle
        room_conflict = CourseSchedule.objects.filter(
            room=self.room,
            day=self.day,
            time_slot=self.time_slot
        ).exclude(pk=self.pk)

        if room_conflict.exists():
            errors["room"] = "Cette salle est déjà utilisée à ce créneau."

        # Salle adaptée au type de cours
        if self.subject and self.room:
            if self.subject.course_type == "TP" and self.room.room_type != "TP":
                errors["room"] = "Pour un TP, il est préférable de choisir une salle TP / laboratoire."

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.subject.name} - {self.level.name} - {self.day} - {self.time_slot}"