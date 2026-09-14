from django.db import models


class Student(models.Model):
    student_id = models.AutoField(primary_key=True)

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=6, null=True, blank=True)
    email = models.EmailField(max_length=100)
    enrollment_date = models.DateField()
    phone = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'students'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


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