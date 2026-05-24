from django.urls import path
from . import views

urlpatterns = [
    # 1. Your home page or book list view
    path('', views.book_list, name='book_list'),
    
    # 2. THE MISSING ROUTE: The individual book details view page
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    
    # 3. Your borrow action route
    path('book/<int:book_id>/borrow/', views.request_borrow, name='request_borrow'),
]