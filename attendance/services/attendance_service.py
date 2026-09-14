from datetime import date

from attendance.models import Attendance


def record_arrival(student_id, arrival_time):
    today = date.today()

    attendance, created = Attendance.objects.get_or_create(
        student_id=student_id,
        date=today,
        defaults={
            'arrival_time': arrival_time,
            'status': 'PRESENT',
            'comment': '',
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
        'attendance': attendance,
    }
def record_departure(student_id, departure_time):
    today = date.today()

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