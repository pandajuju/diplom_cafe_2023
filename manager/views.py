from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404
from django.views.generic import ListView, UpdateView
from coffee.models import Reservation, Post
from .forms import ReservationEditForm
from django.urls import reverse_lazy, reverse


class ManagerAccessMixin(UserPassesTestMixin):
    """
    Mixin for granting access to manager users only.

    Methods:
        test_func() -> bool: Checks if the current user belongs to the 'manager' group.
    """

    def test_func(self) -> bool:
        """
        Checks if the current user belongs to the 'manager' group.

        Returns:
            bool: True if the user is a manager, False otherwise.
        """
        return self.request.user.groups.filter(name='manager').exists()


class ManagerIndex(LoginRequiredMixin, ManagerAccessMixin, ListView):
    """
    View for displaying the manager index page.

    Attributes:
        template_name (str): The name of the template used for rendering the page.
        login_url (str): The URL where users will be redirected if not logged in.
        model: The model class to use for retrieving data.
        context_object_name (str): The name of the variable to use in the template for the object list.
    """
    template_name = 'manager_index.html'
    login_url = '/login/'
    model = Reservation
    context_object_name = 'reservations'

    def get_queryset(self):
        """
        Retrieves the queryset of reservations.

        Returns:
            QuerySet: The queryset of reservations.
        """
        return Reservation.objects.filter(is_precessed=False).order_by('date', 'time')

    def get_context_data(self, **kwargs) -> dict:
        """
        Retrieves context data for rendering the template.

        Returns:
            dict: The context data.
        """
        context = super().get_context_data(**kwargs)
        try:
            recent_posts = Post.objects.order_by('-date_posted')[:2]
            context['recent_posts'] = recent_posts
        except Exception:
            raise Http404("Error processing requests")
        return context


class EditReservation(LoginRequiredMixin, ManagerAccessMixin, UpdateView):
    """
    View for editing a reservation.

    Attributes:
        template_name (str): The name of the template used for rendering the page.
        login_url (str): The URL where users will be redirected if not logged in.
        model: The model class to use for retrieving data.
        form_class: The form class to use for displaying and processing the data.
        success_url (str): The URL where users will be redirected after successful form submission.
    """
    template_name = 'edit_reservation.html'
    login_url = '/login'
    model = Reservation
    form_class = ReservationEditForm
    success_url = reverse_lazy('manager:home')

    def get_context_data(self, **kwargs) -> dict:
        """
        Retrieves context data for rendering the template.

        Returns:
            dict: The context data.
        """
        context = super().get_context_data(**kwargs)
        try:
            recent_posts = Post.objects.order_by('-date_posted')[:2]
            context['recent_posts'] = recent_posts
        except Exception:
            raise Http404("Error processing requests")
        return context
