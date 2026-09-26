from datetime import date, time

from attendance.models import Attendance, Student


ARRIVAL_CUTOFF = time(8, 0)
ABSENCE_CUTOFF = time(8, 30)


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

    if not student.is_active:
        return {
            'success': False,
            'message': 'Student is inactive',
            'attendance': None,
        }

    existing_attendance = Attendance.objects.filter(
        student_id=student_id,
        date=today
    ).first()

    if existing_attendance:
        if existing_attendance.status == 'ABSENT':
            return {
                'success': False,
                'message': 'Student is already marked absent',
                'attendance': existing_attendance,
            }

        return {
            'success': False,
            'message': 'Already scanned',
            'attendance': existing_attendance,
        }

    comment = ''

    if student.student_type == 'DAY_SCHOLAR':
        if arrival_time <= ARRIVAL_CUTOFF:
            comment = 'ON TIME'
        else:
            comment = 'LATE'

    attendance = Attendance.objects.create(
        student_id=student_id,
        date=today,
        arrival_time=arrival_time,
        status='PRESENT',
        comment=comment,
    )

    return {
        'success': True,
        'message': 'Arrival recorded',
        'student_name': f'{student.first_name} {student.last_name}',
        'student_type': student.student_type,
        'attendance': attendance,
    }


def record_departure(student_id, departure_time):
    today = date.today()

    try:
        student = Student.objects.get(student_id=student_id)
    except Student.DoesNotExist:
        return {
            'success': False,
            'message': 'Student not found',
            'attendance': None,
        }

    if not student.is_active:
        return {
            'success': False,
            'message': 'Student is inactive',
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

    if attendance.status == 'ABSENT':
        return {
            'success': False,
            'message': 'Student is marked absent',
            'attendance': attendance,
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

    if current_time <= ABSENCE_CUTOFF:
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