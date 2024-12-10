from django.urls import path

from carLoudApp.interactions import views


urlpatterns = [
    path('posts/post/<int:post_pk>/like/', views.LikeToggleAPIView.as_view(), name='like-api'),
    path('accounts/account/<int:account_pk>/follow/', views.FollowToggleAPIView.as_view(), name='follow-api'),
    path('comments/comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment-delete-api'),
    path('comments/comment/<int:pk>/edit/', views.CommentEditView.as_view(), name='comment-edit-api'),
    path('comments/add/', views.CommentCreateView.as_view(), name='comment-create-api'),

]
