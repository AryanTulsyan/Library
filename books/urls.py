from django.urls import path
from . import views

from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('request-borrow/<int:book_id>/', views.request_borrow, name='request_borrow'),
    # 🌟 ADD THIS LINE TO FIX THE REVERSE MATCH ERROR
    path('about/', views.about_page, name='about_page'),
]