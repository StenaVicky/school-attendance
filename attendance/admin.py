from django.contrib import admin
from .models import Student, Attendance, FingerprintEnrollment


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'student_id',
        'first_name',
        'last_name',
        'email',
        'phone',
        'gender',
        'student_type',
        'enrollment_date',
        'is_active',
        'fingerprint_count',
        'fingerprint_status',
    )

    list_filter = (
        'student_type',
        'gender',
        'is_active',
        'enrollment_date',
    )

    search_fields = (
        'student_id',
        'first_name',
        'last_name',
        'email',
        'phone',
    )

    ordering = (
        '-enrollment_date',
    )

    list_per_page = 25

    @admin.display(description='Fingerprint Count')
    def fingerprint_count(self, obj):
        return obj.fingerprintenrollment_set.filter(
            is_active=True
        ).count()

    @admin.display(description='Fingerprint Status')
    def fingerprint_status(self, obj):
        count = self.fingerprint_count(obj)

        if count >= 2:
            return 'Ready'
        elif count == 1:
            return 'Needs another finger'
        return 'Not enrolled'


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = (
        'student_id',
        'student_name',
        'student_phone',
        'date',
        'arrival',
        'departure',
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
        'student__student_id',
        'student__first_name',
        'student__last_name',
        'student__phone',
    )

    ordering = (
        '-date',
        '-arrival',
    )

    list_per_page = 25

    @admin.display(description='Student Name')
    def student_name(self, obj):
        return f"{obj.student.first_name} {obj.student.last_name}"

    @admin.display(description='Student Phone')
    def student_phone(self, obj):
        return obj.student.phone


@admin.register(FingerprintEnrollment)
class FingerprintEnrollmentAdmin(admin.ModelAdmin):
    list_display = (
        'student_id',
        'student_name',
        'student_type',
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
        'student__student_id',
        'student__first_name',
        'student__last_name',
        'student__phone',
    )

    ordering = (
        '-enrolled_at',
    )

    list_per_page = 25

    @admin.display(description='Student Name')
    def student_name(self, obj):
        return f"{obj.student.first_name} {obj.student.last_name}"

    @admin.display(description='Student Type')
    def student_type(self, obj):
        return obj.student.student_type