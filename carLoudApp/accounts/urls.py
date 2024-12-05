from django.contrib.auth.views import LogoutView
from django.urls import path
from carLoudApp.accounts import views


urlpatterns = [
    path('resend-email/', views.resend_verification_email, name='user-resend-email'),
    path('register/', views.UserRegisterView.as_view(), name='user-register'),
    path('login/', views.user_login, name='user-login'),
    path('account/<int:pk>/details/', views.UserDetailsView.as_view(), name='user-details'),
    path('account/<int:pk>/logout/', LogoutView.as_view(), name='user-logout'),
    path('account/<uidb64>/<token>/', views.activate_user, name='user-activate'),

]
