"""
URL configuration for librarysite project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Route for your beautiful new Jazzmin admin dashboard
    path('admin/', admin.site.urls),
    
    # Route that connects your main domain to your books catalog pages
    path('', include('books.urls')),
]