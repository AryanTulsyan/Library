"""
URL configuration for librarysite project.
"""
from django.contrib import admin
from django.urls import path, include  # Added include here

urlpatterns = [
    # Admin panel route
    path('admin/', admin.site.urls),
    
    # Forward all homepage and root traffic to your books application
    path('', include('books.urls')),
]