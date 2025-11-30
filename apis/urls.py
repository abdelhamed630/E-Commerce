from .views import catagroy_api, product_api, regeister_api,activation_view
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


app_name = 'apis'

urlpatterns = [ 
    path('categories/', catagroy_api, name='category_api'),
    path('categories/<str:slug>/', catagroy_api, name='category_api'),
    path('products/', product_api, name='product_api'),
    path('products/<str:slug>/', product_api, name='product_api'),
    path('register/', regeister_api, name='register_api'),
    path('activate/<uidb64>/<token>/', activation_view, name='activate_account'),
    path('token/',TokenObtainPairView.as_view(), name ='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name ='token_refresh'),
]
