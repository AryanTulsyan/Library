from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Book, BorrowRequest

def book_list(request):
    # Grab search parameter 'q' from user submission form
    query = request.GET.get('q')
    
    if query:
        # Filter if search criteria is filled
        books = Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query))
    else:
        # Serve comprehensive collection default state
        books = Book.objects.all()
        
    return render(request, 'books/book_list.html', {'books': books})

def request_borrow(request, book_id):
    # Ensure the item exists in the database
    book = get_object_or_404(Book, id=book_id)
    
    # FIX: Changed from 'book.is_available' to 'book.available' to match models.py
    if book.available:  
        # 1. Flip the book availability status flag
        book.available = False
        book.save()
        
        # 2. Log a transaction entry in your BorrowRequest table
        # If a logged-in admin tests it, use their profile. Otherwise, fall back to the first available user.
        fallback_user = request.user if request.user.is_authenticated else User.objects.first()
        
        if fallback_user:
            BorrowRequest.objects.create(
                book=book,
                user=fallback_user,
                status='APPROVED' # Automatically approve it since there's no login gate
            )
        
        messages.success(request, f'You have successfully borrowed "{book.title}"!')
    else:
        messages.error(request, f'Sorry, "{book.title}" is already borrowed.')
        
    return redirect('book_list')