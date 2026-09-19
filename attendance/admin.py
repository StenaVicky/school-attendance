from django.contrib import admin
from .models import Attendance, Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "student_id",
        "first_name",
        "last_name",
        "student_type",
        "date_of_birth",
        "gender",
        "enrollment_date",
    )
    search_fields = (
        "first_name",
        "last_name",
    )
    list_filter = (
        "student_type",
        "gender",
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
