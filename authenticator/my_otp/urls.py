from django.urls import path
from .views import Login, create_user_view, login_successful_view

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('login_successful/', login_successful_view, name='login_successful'),
    path('create_user/', create_user_view, name='create_user')
     
]
