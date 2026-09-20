from django.contrib import admin
from .models import Student, Attendance, FingerprintEnrollment


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'student_id',
        'first_name',
        'last_name',
        'student_type',
        'is_active',
    )

    list_filter = (
        'student_type',
        'is_active',
    )

    search_fields = (
        'first_name',
        'last_name',
    )


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = (
        'student_id',
        'date',
        'arrival_time',
        'departure_time',
        'status',
        'scan_method',
        'comment',
    )

    list_filter = (
        'date',
        'status',
        'scan_method',
    )


@admin.register(FingerprintEnrollment)
class FingerprintEnrollmentAdmin(admin.ModelAdmin):
    list_display = (
        'student_id',
        'finger',
        'enrolled_at',
        'is_active',
    )

    list_filter = (
        'finger',
        'is_active',
    )