from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    
    path('borrow/<int:book_id>/', views.request_borrow, name='request_borrow'),
]