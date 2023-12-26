from django.shortcuts import render
from django.views.generic import TemplateView


def home(request):
    return render(request, 'coffee_home.html')


def menu(request):
    return render(request, 'coffee_menu.html')


def services(request):
    return render(request, 'coffee_services.html')


def blog(request):
    return render(request, 'coffee_blog.html')


def about(request):
    return render(request, 'coffee_about.html')


def contact(request):
    return render(request, 'coffee_contact.html')


def shop(request):
    return render(request, 'coffee_shop.html')


def card(request):
    return render(request, 'coffee_card.html')


def checkout(request):
    return render(request, 'coffee_checkout.html')


def blog_single(request):
    return render(request, 'coffee_blog_single.html')