from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Book

def book_list(request):
    # Fetch all books from the database
    books = Book.objects.all()
    
    # Send the books to the template
    # Django automatically includes 'request.user' here behind the scenes
    return render(request, 'books/book_list.html', {'books': books})

@login_required
def request_borrow(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    # Check your custom field name here (e.g., is_available or available)
    if book.is_available:  
        book.is_available = False
        book.save()
        messages.success(request, f'You have successfully borrowed "{book.title}"!')
    else:
        messages.error(request, f'Sorry, "{book.title}" is already borrowed.')
        
    return redirect('book_list')