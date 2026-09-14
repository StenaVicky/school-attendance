from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse

from attendance.services.attendance_service import (
    record_arrival,
    record_departure,
)
from datetime import datetime


def record_student_arrival(request, student_id):
    arrival_time = datetime.now().time()

    result = record_arrival(student_id, arrival_time)

    return JsonResponse({
        'success': result['success'],
        'message': result['message'],
    })
def record_student_departure(request, student_id):
    departure_time = datetime.now().time()

    result = record_departure(student_id, departure_time)

    return JsonResponse({
        'success': result['success'],
        'message': result['message'],
    })