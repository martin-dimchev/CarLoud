from django.contrib.auth.views import LogoutView
from django.urls import path
from carLoudApp.accounts import views
from carLoudApp.accounts.views import FollowToggleView

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='user-register'),
    path('login/', views.UserLoginView.as_view(), name='user-login'),
    path('account/<int:pk>/details/', views.UserDetailsView.as_view(), name='user-details'),
    path('account/<int:pk>/logout/', LogoutView.as_view(), name='user-logout'),
    path('account/<int:pk>/follow', FollowToggleView.as_view(), name='user-follow'),
]