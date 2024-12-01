from django.urls import path
from carLoudApp.interactions import views

urlpatterns = [
    path('post/<int:image_pk>/like/', views.ToggleLikeAPIView.as_view(), name='like'),
    path('post/<int:image_pk>/comments/comment/<int:comment_pk>/delete', views.CommentDeleteView.as_view(),
         name='comment-delete'),
    path('post/<int:image_pk>/comments/comment/<int:comment_pk>/edit', views.CommentEditView.as_view(), name='comment-edit'),
    path('post/<int:image_pk>/comment/add/', views.CommentCreateView.as_view(), name='comment-create'),

    path('post/<int:image_pk>/comments', views.CommentsListView.as_view(), name='comment-section'),

]
