from django import forms
from .models import Reservation, UserData


class ReservationForm(forms.ModelForm):
    """
    Form for making table reservations.

    Attributes:
        name (forms.CharField): Field for entering the first name of the customer.
        last_name (forms.CharField): Field for entering the last name of the customer.
        date (forms.DateField): Field for selecting the date of the reservation.
        time (forms.TimeField): Field for selecting the time of the reservation.
        phone (forms.CharField): Field for entering the phone number of the customer.
        message (forms.CharField): Field for entering additional message for the reservation (optional).
    """

    name = forms.CharField(label='name', widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'Your Name',
               'data-rule': 'minlength:4',
               'data-msg': 'Please enter at least 4 chars'}))

    last_name = forms.CharField(label='last_name', widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'Your Last Name',
               'data-rule': 'minlength:4',
               'data-msg': 'Please enter at least 4 chars'}))

    date = forms.DateField(label='date', widget=forms.DateInput(
        attrs={'placeholder': 'YYYY-MM-DD',
               'class': 'form-control',
               'id': 'date',
               'data-rule': 'minlength:4',
               'data-msg': 'Please enter at least 4 chars'}))

    time = forms.TimeField(label='time', input_formats=['%I:%M%p', '%I:%M %p', '%I:%M%p', '%I:%M %p'],
                           widget=forms.TimeInput(attrs={'placeholder': 'HH:MMam/pm'}),
                           )

    phone = forms.CharField(label='phone', widget=forms.TextInput(attrs={'placeholder': 'Your Phone',
                                                                         'class': 'form-control',
                                                                         'id': 'phone',
                                                                         'data-rule': 'minlength:4',
                                                                         'data-msg': 'Please enter a valid phone: '
                                                                                     '0xxxxxxxxx'}))

    message = forms.CharField(label='message', required=False, widget=forms.Textarea(
        attrs={'placeholder': 'Message',
               'class': 'form-control',
               'rows': '5'}))

    class Meta:
        model = Reservation
        fields = ('name', 'last_name', 'date', 'time', 'phone', 'message')


class BillingDetailsForm(forms.ModelForm):
    """
    Form for entering billing details.

    Attributes:
        first_name (forms.CharField): Field for entering the first name of the customer.
        last_name (forms.CharField): Field for entering the last name of the customer.
        street_name (forms.CharField): Field for entering the street name of the customer.
        house_number (forms.CharField): Field for entering the house number of the customer.
        phone (forms.CharField): Field for entering the phone number of the customer.
        email_address (forms.EmailField): Field for entering the email address of the customer.
    """
    first_name = forms.CharField(label='first name', widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'Your First Name',
               'data-rule': 'minlength:4',
               'data-msg': 'Please enter at least 4 chars'}))

    last_name = forms.CharField(label='last name', widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'Your Last Name',
               'data-rule': 'minlength:4',
               'data-msg': 'Please enter at least 4 chars'}))

    street_name = forms.CharField(label='Street Name', widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'Street Name',
               'data-rule': 'minlength:4',
               'data-msg': 'Please enter at least 4 chars'}))

    house_number = forms.CharField(label='House Number', widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'Your House Number',
               'data-rule': 'minlengs:1',
               'data-msg': 'Please enter a your number house'}))

    phone = forms.CharField(label='phone', widget=forms.TextInput(
        attrs={'placeholder': 'Your Phone',
               'class': 'form-control',
               'id': 'phone',
               'data-rule': 'minlen:4',
               'data-msg': 'Please enter a valid phone: 0xxxxxxxxx'}))

    email_address = forms.EmailField(label='email', widget=forms.EmailInput(
        attrs={'placeholder': 'Your Email',
               'class': 'form-control',
               'id': 'email',
               'data-rule': 'email',
               'data-msg': 'Please enter a valid email'}))

    class Meta:
        model = UserData
        fields = ['first_name', 'last_name', 'street_name', 'house_number', 'phone', 'email_address']
