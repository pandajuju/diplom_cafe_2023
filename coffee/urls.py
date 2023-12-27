from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
# from .views import IndexPage

app_name = 'coffee'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('services/', views.services, name='services'),
    path('blog/', views.blog, name='blog'),
    path('blog/<int:pk>/', views.blog_single, name='blog_single'),
    path('about/', views.about, name='about'),
    path('shop/', views.shop, name='shop'),
    path('card/', views.card, name='card'),
    path('checkout/', views.checkout, name='checkout'),
    path('contact/', views.contact, name='contact'),

]

