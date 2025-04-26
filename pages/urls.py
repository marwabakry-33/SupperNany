from django.urls import path
from . import views  
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('pre-register-child/', views.PreRegisterChildAPIView.as_view(), name='pre-register-child'),
    path('register-child/', views.RegisterChildAPIView.as_view(), name='register-child'),  
    path('userinfo', views.current_user, name='userinfo'),
    path('logout', views.logout, name='logout'),
    #path('public_data/',views.public_data_view, name='public_data'),
    path('login/', views.user_login.as_view(), name='login'),
    # طلب إعادة تعيين كلمة المرور (طلب البريد الإلكتروني)
    path('request_password/', views.RequestPasswordResetAPIView.as_view(), name='password_reset_done'),
    # إعادة تعيين كلمة المرور
    path('reset_password/', views.ResetPasswordAPIView.as_view(), name='reset_password'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

