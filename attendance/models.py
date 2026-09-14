
from django.db import models


class Attendance(models.Model):
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

