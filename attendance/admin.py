from django.contrib import admin
from .models import Student, Attendance, FingerprintEnrollment


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'student_id',
        'first_name',
        'last_name',
        'email',
        'gender',
        'student_type',
        'is_active',
        'fingerprint_count',
        'fingerprint_status',
    )

    list_filter = (
        'student_type',
        'gender',
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
        return obj.fingerprintenrollment_set.filter(
            is_active=True
        ).count()

    fingerprint_count.short_description = 'Fingerprints'

    def fingerprint_status(self, obj):
        count = obj.fingerprintenrollment_set.filter(
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
        'student_name',
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

    search_fields = (
        'student_id',
    )

    ordering = (
        '-date',
        '-arrival_time',
    )

    def student_name(self, obj):
        try:
            student = Student.objects.get(student_id=obj.student_id)
            return f'{student.first_name} {student.last_name}'
        except Student.DoesNotExist:
            return 'Unknown student'

    student_name.short_description = 'Student Name'


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
        'enrolled_at',
    )

    search_fields = (
        'student_id',
    )

    ordering = (
        '-enrolled_at',
    )

    def student_name(self, obj):
        try:
            student = Student.objects.get(student_id=obj.student_id)
            return f'{student.first_name} {student.last_name}'
        except Student.DoesNotExist:
            return 'Unknown student'

    student_name.short_description = 'Student Name'