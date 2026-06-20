from django.contrib import admin
from .models import Department, Section, Level, Teacher, Subject, Room, TimeSlot, CourseSchedule

admin.site.register(Department)
admin.site.register(Section)
admin.site.register(Level)
admin.site.register(Teacher)
admin.site.register(Subject)
admin.site.register(Room)
admin.site.register(TimeSlot)
admin.site.register(CourseSchedule)