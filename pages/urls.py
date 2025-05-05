from django.urls import path
from . import views  
from django.contrib.auth import views as auth_views

from .views import TaskList, TaskDetail

urlpatterns = [
    path('register/', views.register, name='register'),
    path('pre-register-child/', views.PreRegisterChildAPIView.as_view(), name='pre-register-child'),
    path('register-child/', views.RegisterChildAPIView.as_view(), name='register-child'),  
    path('userinfo', views.current_user, name='userinfo'),
    #path('public_data/',views.public_data_view, name='public_data'),
    path('login/', views.user_login, name='login'),
    # طلب إعادة تعيين كلمة المرور (طلب البريد الإلكتروني)
    path('request_password/', views.RequestPasswordResetAPIView, name='password_reset_done'),
    # إعادة تعيين كلمة المرور
    path('reset_password/', views.ResetPasswordAPIView, name='reset_password'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('task/',TaskList.as_view(), name='task'),
    path('tasks/<int:pk>/',TaskDetail.as_view(), name='task-detail'),  # لقراءة، تحديث وحذف مهمة معينة

    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]


