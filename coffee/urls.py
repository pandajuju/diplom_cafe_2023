from django.urls import path

from .views import *

app_name = 'coffee'

urlpatterns = [
    path('', IndexPage.as_view(), name='home'),
    path('menu/', MenuPage.as_view(), name='menu'),
    path('book_table/', BookTableMultiPageView.as_view(), name='book_table'),
    path('book_table/<int:step>/', BookTableMultiPageView.as_view(), name='book_table_step'),
    path('services/', ServicesPage.as_view(), name='services'),
    path('blog/', BlogPage.as_view(), name='blog'),
    path('blog/<int:id>/', BlogSinglePage.as_view(), name='blog_single'),
    path('about/', AboutPage.as_view(), name='about'),
    path('contact/', ContactPage.as_view(), name='contact'),
    path('shop/', ShopPage.as_view(), name='shop'),
    path('cart/', CartPage.as_view(), name='cart'),
    path('add-to-cart/', AddToCartView.as_view(), name='add_to_cart'),
    path('remove_from_cart/', RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('update_cart/', UpdateCartView.as_view(), name='update_cart'),
    path('checkout/', CheckoutPage.as_view(), name='checkout'),
]