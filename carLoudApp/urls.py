from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('carLoudApp.common.urls')),
    path('accounts/', include('carLoudApp.accounts.urls')),
    path('projects/', include('carLoudApp.projects.urls')),
    path('api/', include('carLoudApp.interactions.urls')),

]
