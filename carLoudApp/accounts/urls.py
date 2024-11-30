from django.contrib.auth.views import LogoutView
from django.urls import path
from carLoudApp.accounts import views
from carLoudApp.accounts.views import user_login

urlpatterns = [
    path('resend-email/', views.resend_verification_email, name='user-resend-email'),
    path('register/', views.UserRegisterView.as_view(), name='user-register'),
    path('login/', user_login, name='user-login'),
    path('account/<int:pk>/details/', views.UserDetailsView.as_view(), name='user-details'),
    path('account/<int:pk>/logout/', LogoutView.as_view(), name='user-logout'),
    path('account/<int:pk>/follow', views.FollowToggleView.as_view(), name='user-follow'),
    path('account/<uidb64>/<token>/', views.activate_user, name='user-activate'),

]
