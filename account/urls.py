from django.urls import path
from account import views

urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name='user-register'),
    path('activate/<str:uidb64>/<str:token>/', views.ActivateAccountView.as_view(), name='activate'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('password-reset/', views.PasswordResetview.as_view(), name="password-reset"),
    path('password-reset-confirm/<str:uidb64>/<str:token>/', views.PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    
]