from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('request-borrow/<int:book_id>/', views.request_borrow, name='request_borrow'),
    # 🌟 Make sure this line is present:
    path('about/', views.about_page, name='about_page'),
]