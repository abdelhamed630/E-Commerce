from django.urls import path
from . import views
app_name = 'store'

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<product_slug>/', views.product_detail, name='product_detail'),
    path('category/<category_slug>/', views.home, name='product_by_category'),
    path('search/', views.search, name='search'),
    path('why/',views.why_us, name='why_us'),
    path('about/',views.about, name='about_us'),
    path('testimonials/',views.testimonials, name='testimonials'),
]