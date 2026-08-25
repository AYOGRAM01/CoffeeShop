from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('coffee/<int:coffee_id>/', views.coffee_detail, name='coffee_detail'),
    path('add_to_cart/<int:coffee_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('search/', views.search, name='search'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment/', views.payment, name='payment'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manage_coffee/', views.manage_coffee, name='manage_coffee'),
    path('confirm_order/<int:order_id>/', views.confirm_order, name='confirm_order'),
    path('view_orders/', views.view_orders, name='view_orders'),
    path('view_contacts/', views.view_contacts, name='view_contacts'),
]
