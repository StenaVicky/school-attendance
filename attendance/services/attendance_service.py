from datetime import date, time

from attendance.models import Attendance, Student


def record_arrival(student_id, arrival_time):
    today = date.today()

    try:
        student = Student.objects.get(student_id=student_id)
    except Student.DoesNotExist:
        return {
            'success': False,
            'message': 'Student not found',
            'attendance': None,
        }

    comment = ''

    if student.student_type == 'DAY_SCHOLAR':
        if arrival_time <= time(8, 0):
            comment = 'ON TIME'
        else:
            comment = 'LATE'

    attendance, created = Attendance.objects.get_or_create(
        student_id=student_id,
        date=today,
        defaults={
            'arrival_time': arrival_time,
            'status': 'PRESENT',
            'comment': comment,
        }
    )

    if not created:
        return {
            'success': False,
            'message': 'Already scanned',
            'attendance': attendance,
        }

    return {
        'success': True,
        'message': 'Arrival recorded',
        'student_type': student.student_type,
        'attendance': attendance,
    }


def record_departure(student_id, departure_time):
    today = date.today()

    try:
        Student.objects.get(student_id=student_id)
    except Student.DoesNotExist:
        return {
            'success': False,
            'message': 'Student not found',
            'attendance': None,
        }

    try:
        attendance = Attendance.objects.get(
            student_id=student_id,
            date=today
        )
    except Attendance.DoesNotExist:
        return {
            'success': False,
            'message': 'No arrival scan found',
            'attendance': None,
        }

    if attendance.departure_time is not None:
        return {
            'success': False,
            'message': 'Already scanned',
            'attendance': attendance,
        }

    attendance.departure_time = departure_time
    attendance.save(update_fields=['departure_time'])

    return {
        'success': True,
        'message': 'Departure recorded',
        'attendance': attendance,
    }


def mark_absent_students(current_time):
    today = date.today()
    cutoff_time = time(8, 30)

    if current_time <= cutoff_time:
        return {
            'success': False,
            'message': 'Attendance cutoff has not been reached',
            'absent_count': 0,
        }

    absent_count = 0

    students = Student.objects.filter(is_active=True)

    for student in students:
        attendance_exists = Attendance.objects.filter(
            student_id=student.student_id,
            date=today
        ).exists()

        if not attendance_exists:
            Attendance.objects.create(
                student_id=student.student_id,
                date=today,
                status='ABSENT',
                comment='ABSENT',
            )
            absent_count += 1

    return {
        'success': True,
        'message': 'Absent students marked',
        'absent_count': absent_count,
    }