from attendance.models import FingerprintEnrollment, Student


def enroll_fingerprint(student_id, finger):
    try:
        student = Student.objects.get(student_id=student_id)
    except Student.DoesNotExist:
        return {
            'success': False,
            'message': 'Student not found',
            'enrollment': None,
        }

    if not student.is_active:
        return {
            'success': False,
            'message': 'Cannot enroll fingerprint for an inactive student',
            'enrollment': None,
        }

    active_enrollments = FingerprintEnrollment.objects.filter(
        student_id=student_id,
        is_active=True
    )

    if active_enrollments.count() >= 2:
        return {
            'success': False,
            'message': 'Student already has two active fingerprints',
            'enrollment': None,
        }

    already_enrolled = FingerprintEnrollment.objects.filter(
        student_id=student_id,
        finger=finger,
        is_active=True
    ).exists()

    if already_enrolled:
        return {
            'success': False,
            'message': 'This finger is already enrolled for this student',
            'enrollment': None,
        }

    enrollment = FingerprintEnrollment.objects.create(
        student_id=student_id,
        finger=finger,
    )

    return {
        'success': True,
        'message': 'Fingerprint enrolled successfully for this student',
        'enrollment': enrollment,
    }