from django.urls import path
from .views import ManagerIndex, EditReservation

app_name = 'manager'

urlpatterns = [
    path('', ManagerIndex.as_view(), name='home'),
    path('reservations/<int:pk>/', EditReservation.as_view(), name='edit_reservations')
]