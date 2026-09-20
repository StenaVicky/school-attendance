
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
        'fingerprint_count',
    )

    list_filter = (
        'student_type',
        'is_active',
    )

    search_fields = (
        'student_id',
        'first_name',
        'last_name',
    )

    def fingerprint_count(self, obj):
        return FingerprintEnrollment.objects.filter(
            student_id=obj.student_id,
            is_active=True
        ).count()

    fingerprint_count.short_description = 'Fingerprints'


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

