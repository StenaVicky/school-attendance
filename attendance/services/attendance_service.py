from datetime import date, time

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