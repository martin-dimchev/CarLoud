from django.urls import path
from carLoudApp.projects import views

urlpatterns = [
    path('garage/<int:pk>', views.GarageListView.as_view(), name='user-garage'),
    path('create/', views.ProjectCreateView.as_view(), name='project-create'),
    path('project/<int:pk>/delete/', views.project_delete, name='project-delete'),
    path('project/<int:pk>/images/add/', views.ProjectImageCreateView.as_view(), name='project-image-add'),
    path('project/<int:pk>/details', views.ProjectDetailView.as_view(), name='project-details'),
    path('project/<int:pk>/edit', views.ProjectUpdateView.as_view(), name='project-edit'),
    path('project/<int:pk>/images/image/<int:image_pk>', views.ProjectImageDetailView.as_view(), name='project-image'),

]