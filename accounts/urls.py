from django.urls import path
from . import views
from . import password_reset

app_name = 'account'
urlpatterns = [
    path('login', views.login_view, name='login'),
    # ENTFERNT: path('register', views.register, name='signup'),  # Ersetzt durch /ge/kroatien/partner-werden/
    path('logout', views.logout_view, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('agents/<str:pk>/', views.agents, name='agents'),
    path('verify-email/', views.verifyEmail, name='verify_email'),
    path('verify-otp/', views.verifyOTP, name='verify_otp'),
    path('forget-password/', views.forgetPassword, name='forget_password'),
    path('reset-password/', views.resetPassword, name='reset_password'),
    
    # SECURE PASSWORD RESET SYSTEM
    path('password-reset/', password_reset.password_reset_request, name='password_reset_request'),
    path('password-reset/done/', password_reset.password_reset_done, name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/', password_reset.password_reset_confirm, name='password_reset_confirm'),
    path('password-reset/complete/', password_reset.password_reset_complete, name='password_reset_complete'),
]
