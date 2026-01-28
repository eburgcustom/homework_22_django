from django.urls import path
from . import views
from users.views import email_verification

app_name = 'users'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('email-confirm/<str:token>/', email_verification, name='email-confirm')
]
