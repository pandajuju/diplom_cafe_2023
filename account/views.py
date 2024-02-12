from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from .forms import UserRegistrationForm, UserLoginForm


def logout_user(request) -> redirect:
    """
    Logs out the current user and redirects to the home page.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponseRedirect: Redirects to the home page.
    """
    logout(request)
    return redirect(reverse('coffee:home'))


class RegisterUser(CreateView):
    """
    View for registering a new user.

    Attributes:
        form_class (Form): The form class for user registration.
        template_name (str): The template name for the registration page.
        success_url (str): The URL to redirect to after successful registration.
    """
    form_class = UserRegistrationForm
    template_name = 'registration.html'
    success_url = reverse_lazy('login')


class LoginUser(LoginView):
    """
    View for user login.

    Attributes:
        form_class (Form): The form class for user login.
        template_name (str): The template name for the login page.
    """
    form_class = UserLoginForm
    template_name = 'login.html'

    def get_success_url(self) -> str:
        """
        Returns the URL to redirect to after successful login.

        Returns:
            str: The URL to redirect to.
        """
        return self.request.GET.get('next') or self.request.POST.get('next') or '/'