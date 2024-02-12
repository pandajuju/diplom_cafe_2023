from django import forms
from coffee.models import Reservation


class ReservationEditForm(forms.ModelForm):
    """
    Form for editing reservation details.

    """
    class Meta:
        model = Reservation
        fields = ('is_precessed', 'name', 'last_name', 'date', 'phone', 'message', )

