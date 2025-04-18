from django.urls import path
from . import views  
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('userinfo', views.current_user, name='userinfo'),
    path('logout', views.logout, name='logout'),
    path('public_data/',views.public_data_view, name='public_data'),
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]



