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
        'phone',
        'email',
    )

    ordering = ('-enrollment_date',)
    list_per_page = 25

    @admin.display(description='Fingerprints')
    def fingerprint_count(self, obj):
        return obj.fingerprintenrollment_set.filter(
            is_active=True
        ).count()

    @admin.display(description='Fingerprint Status')
    def fingerprint_status(self, obj):
        count = obj.fingerprintenrollment_set.filter(
            is_active=True
        ).count()

        if count >= 2:
            return 'Ready'
        elif count == 1:
            return 'Needs another finger'
        return 'Not enrolled'


class StudentTypeFilter(admin.SimpleListFilter):
    title = 'Student Type'
    parameter_name = 'student_type'

    def lookups(self, request, model_admin):
        return (
            ('DAY_SCHOLAR', 'Day Scholar'),
            ('BOARDER', 'Boarder'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'DAY_SCHOLAR':
            student_ids = Student.objects.filter(
                student_type='DAY_SCHOLAR'
            ).values_list('student_id', flat=True)

            return queryset.filter(student_id__in=student_ids)

        if self.value() == 'BOARDER':
            student_ids = Student.objects.filter(
                student_type='BOARDER'
            ).values_list('student_id', flat=True)

            return queryset.filter(student_id__in=student_ids)

        return queryset


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = (
        'student_id',
        'student_name',
        'student_phone',
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
        StudentTypeFilter,
    )

    search_fields = ('student_id',)
    search_help_text = 'Search by student ID, name, or phone number.'
    date_hierarchy = 'date'
    ordering = ('-date', '-arrival_time')
    list_per_page = 25

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(
            request, queryset, search_term
        )

        student_ids = Student.objects.filter(
            first_name__icontains=search_term
        ).values_list('student_id', flat=True)

        student_ids = student_ids.union(
            Student.objects.filter(
                last_name__icontains=search_term
            ).values_list('student_id', flat=True)
        )

        student_ids = student_ids.union(
            Student.objects.filter(
                phone__icontains=search_term
            ).values_list('student_id', flat=True)
        )

        queryset |= self.model.objects.filter(
            student_id__in=student_ids
        )

        return queryset, use_distinct

    @admin.display(description='Phone')
    def student_phone(self, obj):
        try:
            student = Student.objects.get(
                student_id=obj.student_id
            )
            return student.phone or 'No phone'
        except Student.DoesNotExist:
            return 'Unknown student'

    @admin.display(
        description='Student Name',
        ordering='student_id'
    )
    def student_name(self, obj):
        try:
            student = Student.objects.get(
                student_id=obj.student_id
            )
            return f'{student.first_name} {student.last_name}'
        except Student.DoesNotExist:
            return 'Unknown student'


@admin.register(FingerprintEnrollment)
class FingerprintEnrollmentAdmin(admin.ModelAdmin):
    list_display = (
        'student_id',
        'student_name',
        'student_phone',
        'student_type',
        'finger',
        'enrolled_at',
        'is_active',
    )

    list_filter = (
        StudentTypeFilter,
        'finger',
        'is_active',
        'enrolled_at',
    )

    search_fields = ('student_id',)
    search_help_text = 'Search by student ID, name, or phone number.'
    ordering = ('-enrolled_at',)
    list_per_page = 25

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(
            request, queryset, search_term
        )

        student_ids = Student.objects.filter(
            first_name__icontains=search_term
        ).values_list('student_id', flat=True)

        student_ids = student_ids.union(
            Student.objects.filter(
                last_name__icontains=search_term
            ).values_list('student_id', flat=True)
        )

        student_ids = student_ids.union(
            Student.objects.filter(
                phone__icontains=search_term
            ).values_list('student_id', flat=True)
        )

        queryset |= self.model.objects.filter(
            student_id__in=student_ids
        )

        return queryset, use_distinct

    @admin.display(
        description='Student Name',
        ordering='student_id'
    )
    def student_name(self, obj):
        try:
            student = Student.objects.get(
                student_id=obj.student_id
            )
            return f'{student.first_name} {student.last_name}'
        except Student.DoesNotExist:
            return 'Unknown student'

    @admin.display(description='Phone')
    def student_phone(self, obj):
        try:
            student = Student.objects.get(
                student_id=obj.student_id
            )
            return student.phone or 'No phone'
        except Student.DoesNotExist:
            return 'Unknown student'

    @admin.display(description='Student Type')
    def student_type(self, obj):
        try:
            student = Student.objects.get(
                student_id=obj.student_id
            )
            return student.get_student_type_display()
        except Student.DoesNotExist:
            return 'Unknown student'