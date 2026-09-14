from django.urls import path
from .views import record_student_arrival

urlpatterns = [
    path('arrival/<int:student_id>/', record_student_arrival, name='record_student_arrival'),
]