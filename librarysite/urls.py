from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView # <-- Add this import

urlpatterns = [
    # Catch favicon requests and safely redirect them to your static folder
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico')),
    
    path('admin/', admin.site.urls),
    path('', include('books.urls')), 
]