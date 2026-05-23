from django.urls import path
from . import views

urlpatterns = [
    # This maps to your homepage catalog view
    path('', views.book_list, name='book_list'),
    
    # This maps the borrow button action to your backend logic
    path('book/<int:book_id>/borrow/', views.request_borrow, name='request_borrow'),
]