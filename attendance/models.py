
from django.db import models
from django.utils import timezone


class Student(models.Model):
    student_id = models.AutoField(primary_key=True)

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=6, null=True, blank=True)
    email = models.EmailField(max_length=100)
    enrollment_date = models.DateField()
    phone = models.CharField(max_length=20, null=True, blank=True)

    STUDENT_TYPE_CHOICES = [
        ('DAY_SCHOLAR', 'Day Scholar'),
        ('BOARDER', 'Boarder'),
    ]

    student_type = models.CharField(
        max_length=20,
        choices=STUDENT_TYPE_CHOICES,
        default='DAY_SCHOLAR',
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        managed = False
        db_table = 'students'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Attendance(models.Model):
    created_at = models.DateTimeField(default=timezone.now)

    SCAN_METHOD_CHOICES = [
        ('FINGERPRINT', 'Fingerprint'),
        ('MANUAL', 'Manual'),
        ('OFFLINE', 'Offline'),
    ]

    scan_method = models.CharField(
        max_length=20,
        choices=SCAN_METHOD_CHOICES,
        default='FINGERPRINT',
    )

    STATUS_CHOICES = [
        ('PRESENT', 'Present'),
        ('ABSENT', 'Absent'),
    ]

    student_id = models.IntegerField()

    date = models.DateField()
    arrival_time = models.TimeField(null=True, blank=True)
    departure_time = models.TimeField(null=True, blank=True)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES
    )

    comment = models.CharField(
        max_length=255,
        blank=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student_id', 'date'],
                name='unique_student_attendance_per_day'
            )
        ]

    def __str__(self):
        return f"Student {self.student_id} - {self.date}"


class FingerprintEnrollment(models.Model):
    FINGER_CHOICES = [
        ('LEFT_THUMB', 'Left Thumb'),
        ('LEFT_INDEX', 'Left Index'),
        ('RIGHT_THUMB', 'Right Thumb'),
        ('RIGHT_INDEX', 'Right Index'),
    ]

    student_id = models.IntegerField()

    finger = models.CharField(
        max_length=20,
        choices=FINGER_CHOICES
    )

    enrolled_at = models.DateTimeField(
        default=timezone.now
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student_id', 'finger'],
                name='unique_student_fingerprint'
            )
        ]

    def __str__(self):
        return f"Student {self.student_id} - {self.finger}"

