from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('visualiser.urls')),  # Include URLs from 'optimizer' app
]