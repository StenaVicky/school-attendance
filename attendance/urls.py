from django.urls import path
from .views import record_student_arrival, record_student_departure

urlpatterns = [
    path(
        'arrival/<int:student_id>/',
        record_student_arrival,
        name='record_student_arrival'
    ),
    path(
        'departure/<int:student_id>/',
        record_student_departure,
        name='record_student_departure'
    ),
]