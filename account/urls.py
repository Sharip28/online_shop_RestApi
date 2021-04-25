from django.urls import path

from account.views import RegistrationView, ActivationView, LoginView, LogoutView, ForgotPasswordView, \
    ForgotPasswordCompleteView

urlpatterns = [
    path('register/',RegistrationView.as_view()),
    path('activate/<str:activation_code>/',ActivationView.as_view()),
    path('login/',LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('forgot_password/', ForgotPasswordView.as_view()),
    path('forgot_password_complete/', ForgotPasswordCompleteView.as_view())
]