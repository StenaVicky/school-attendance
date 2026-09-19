from django.contrib import admin
from .models import Attendance, Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "student_id",
        "first_name",
        "last_name",
    )
    search_fields = (
        "first_name",
        "last_name",
    )


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = (
        "student_id",
        "date",
        "arrival_time",
        "departure_time",
        "status",
        "comment",
    )
    list_filter = (
        "status",
        "date",
    )
