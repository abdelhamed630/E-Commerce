from django.urls import path
from . import views

app_name = 'orders'
urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('pay/<str:order_id>/', views.order_pay_by_vodafone, name='pay_order'),
    path('payment-success/<str:order_id>/', views.payment_success, name='payment_success'),
# urls.py
path('admin/pdf/<str:order_id>/pdf/', views.admin_order_pdf, name='admin_order_pdf')
]