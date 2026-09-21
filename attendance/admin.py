from django.contrib import admin
from .models import Student, Attendance, FingerprintEnrollment


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'student_id',
        'first_name',
        'last_name',
        'email',
        'student_type',
        'is_active',
        'fingerprint_count',
        'fingerprint_status',
    )

    list_filter = (
        'student_type',
        'is_active',
    )

    search_fields = (
        'student_id',
        'first_name',
        'last_name',
        'phone',
        'email',
    )

    def fingerprint_count(self, obj):
        return FingerprintEnrollment.objects.filter(
            student_id=obj.student_id,
            is_active=True
        ).count()

    fingerprint_count.short_description = 'Fingerprints'

    def fingerprint_status(self, obj):
        count = FingerprintEnrollment.objects.filter(
            student_id=obj.student_id,
            is_active=True
        ).count()

        if count >= 2:
            return 'Ready'
        elif count == 1:
            return 'Needs another finger'
        else:
            return 'Not enrolled'

    fingerprint_status.short_description = 'Fingerprint Status'


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
        'student_name',
        'finger',
        'enrolled_at',
        'is_active',
    )

    list_filter = (
        'finger',
        'is_active',
    )

    search_fields = (
        'student_id',
    )

    def student_name(self, obj):
        try:
            student = Student.objects.get(student_id=obj.student_id)
            return f"{student.first_name} {student.last_name}"
        except Student.DoesNotExist:
            return "Student not found"

    student_name.short_description = 'Student Name'