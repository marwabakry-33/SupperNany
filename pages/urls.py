from django.urls import path
from . import views  
from django.contrib.auth import views as auth_views
from .views import*
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import HowToByCategoryView

urlpatterns = [
    path('register/', views.register, name='register'),
   
    path('pre-register-child2/', views.PreRegisterChildAPIView2.as_view(), name='pre-register-child2'),
    
    path('api/child/<int:child_id>/upload-photo/', upload_child_photo),
    path('child/<int:child_id>/photo/', get_child_photo, name='get_child_photo'),
    path('child/<int:child_id>/photo/update/', update_child_photo, name='update_child_photo'),

    path('register-child/', views.RegisterChildAPIView.as_view(), name='register-child'),  
    path('child/<int:pk>/update/', UpdateChildAPIView.as_view(), name='update_child'),

    path('userinfo', views.current_user, name='userinfo'),
    path('api/update-mother/', views.update_mother_profile, name='update_mother'),

    #path('public_data/',views.public_data_view, name='public_data'),
    path('login/', views.user_login, name='login'),
    # طلب إعادة تعيين كلمة المرور (طلب البريد الإلكتروني)
    path('request_password/', views.RequestPasswordResetAPIView, name='password_reset_done'),
    # إعادة تعيين كلمة المرور
    path('reset_password/', views.ResetPasswordAPIView, name='reset_password'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('task/',TaskList.as_view(), name='task'),
    path('tasks/<int:pk>/',TaskDetail.as_view(), name='task-detail'),  # لقراءة، تحديث وحذف مهمة معينة
    path('task/<int:child_id>/',TaskDetail.as_view(), name='task-list-for-child'),
    path('tasks/favorite/<int:child_id>/', FavoriteTasksForChild.as_view(), name='favorite_tasks'),

    path('advice/<str:category>/', RandomAdviceView.as_view(), name='random-advice'),
    path('child/<int:child_id>/', GetChildByIdAPIView.as_view(), name='get_child_by_id'),
    # تسجيل الدخول - يرجع Access و Refresh Token
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # تحديث التوكن - يرجع Access جديد باستخدام Refresh
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('howto/<str:category>/', HowToByCategoryView.as_view(), name='howto-by-category'),
    path('child/<int:child_id>/growth/', create_growth_record, name='create_growth_record'),
    path('child/<int:child_id>/growth/view/', get_growth_records, name='get_growth_records'),
    path('growth-records/<int:child_id>/<int:record_id>/update/', update_growth_record, name='update-growth-record'),

]


