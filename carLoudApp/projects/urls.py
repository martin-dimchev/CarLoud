from django.urls import path

from carLoudApp.projects import views

urlpatterns = [
    path('create/', views.ProjectCreateView.as_view(), name='project-create'),
    path('garage/<int:pk>', views.GarageListView.as_view(), name='user-garage'),
    path('project/<int:pk>/', views.ProjectDetailView.as_view(), name='project-details'),
    path('project/<int:pk>/edit/', views.ProjectEditView.as_view(), name='project-edit'),
    path('project/<int:pk>/delete/', views.project_delete, name='project-delete'),

    path('project/<int:pk>/posts/create/', views.ProjectPostCreateView.as_view(), name='project-image-add'),
    path('project/<int:pk>/posts/post/<int:post_pk>/', views.ProjectPostDetailView.as_view(),
         name='project-post-details'),
    path('project/<int:pk>/posts/post/<int:post_pk>/edit/', views.ProjectPostEditView.as_view(),
         name='project-post-edit'),
    path('project/<int:pk>/posts/post/<int:post_pk>/delete/', views.project_post_delete,
         name='project-post-delete'),
]
