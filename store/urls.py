from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.store_view, name='store'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/checkout/', views.checkout_view, name='checkout'),
    path('cart/checkout/payment/', views.payment_view, name='payment'),
    path('cart/checkout/payment/waiting-confirmation/', views.waiting_confirmation, name='waiting_confirmation'),
    path('purchase-history/', views.purchase_history_view, name='purchase_history'),
    path('login/', views.login_view, name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('register/', views.register_view, name='register'),
]