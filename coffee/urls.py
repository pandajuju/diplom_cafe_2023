from django.urls import path

from .views import *

app_name = 'coffee'

urlpatterns = [
    path('', IndexPage.as_view(), name='home'),
    path('menu/', MenuPage.as_view(), name='menu'),
    path('services/', ServicesPage.as_view(), name='services'),
    path('blog/', BlogPage.as_view(), name='blog'),
    path('blog/<int:id>/', BlogSinglePage.as_view(), name='blog_single'),
    path('about/', AboutPage.as_view(), name='about'),
    path('contact/', ContactPage.as_view(), name='contact'),
    path('shop/', ShopPage.as_view(), name='shop'),
    path('card/', CardPage.as_view(), name='card'),
    path('checkout/', CheckoutPage.as_view(), name='checkout'),
]