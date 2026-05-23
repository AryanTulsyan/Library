from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from .models import Book

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
    # Ensure the item exists in the collection database table
    book = get_object_or_404(Book, id=book_id)
    
    if book.is_available:  
        book.is_available = False
        book.save()
        messages.success(request, f'You have successfully borrowed "{book.title}"!')
    else:
        messages.error(request, f'Sorry, "{book.title}" is already borrowed.')
        
    return redirect('book_list')