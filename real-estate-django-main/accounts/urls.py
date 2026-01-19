from django.urls import path
from . import views
from . import password_reset

app_name = 'account'
urlpatterns = [
    path('login', views.login_view, name='login'),   ## accounts/login (accounts come from main urls.py)
    path('register', views.register, name='signup'),  ## accounts/register
    path('logout', views.logout_view, name='logout'),        ## accounts/logout
    path('dashboard', views.dashboard, name='dashboard'),   ## accounts/dashboard
    path('agents/<str:pk>/', views.agents, name='agents'),   ## accounts/agents
    path('verify-email/', views.verifyEmail, name='verify_email'),
    path('verify-otp/', views.verifyOTP, name='verify_otp'),
    
    # Legacy URLs (redirect to new secure system)
    path('forget-password/', views.forgetPassword, name='forget_password'),
    path('reset-password/', views.resetPassword, name='reset_password'),
    
    # ========================================
    # SECURE PASSWORD RESET SYSTEM
    # Kryptographisch sichere Token-basierte Passwort-Zurücksetzung
    # ========================================
    path('password-reset/', password_reset.password_reset_request, name='password_reset_request'),
    path('password-reset/done/', password_reset.password_reset_done, name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/', password_reset.password_reset_confirm, name='password_reset_confirm'),
    path('password-reset/complete/', password_reset.password_reset_complete, name='password_reset_complete'),
]