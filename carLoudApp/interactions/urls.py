from django.urls import path
from carLoudApp.interactions import views

urlpatterns = [
    path('posts/post/<int:image_pk>/like/', views.ToggleLikeAPIView.as_view(), name='like'),
    path('comments/comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment-delete'),
    path('comments/comment/<int:pk>/edit/', views.CommentEditView.as_view(), name='comment-edit-api'),
    path('comments/add/', views.CommentCreateView.as_view(), name='comment-create-api'),

    path('posts/post/<int:image_pk>/comments/', views.CommentsListView.as_view(), name='comment-section'),

]
