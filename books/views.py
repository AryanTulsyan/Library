from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Book, BorrowRequest

def book_list(request):
    query = request.GET.get('q')
    if query:
        books = Book.objects.filter(title__icontains=query) | Book.objects.filter(author__icontains=query)
    else:
        books = Book.objects.all()
    return render(request, 'books/book_list.html', {'books': books})

@login_required
def request_borrow(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    # Check if the book is actually available right now
    if not book.available:
        messages.error(request, f"Sorry, '{book.title}' is currently checked out!")
        return redirect('book_list')
        
    # Check if this user already has an active pending request for this exact book
    already_requested = BorrowRequest.objects.filter(user=request.user, book=book, status='PENDING').exists()
    if already_requested:
        messages.warning(request, "You already have a pending payment request for this book.")
        return redirect('book_list')

    # Create the request using your clean model structure
    BorrowRequest.objects.create(
        book=book,
        user=request.user,
        status='PENDING' # Matches your model key exactly
    )
    
    messages.success(request, f"Your request for '{book.title}' was sent! Please ensure payment is transferred via the QR code.")
    return redirect('book_list')

def about_page(request):
    return render(request, 'books/about.html')
# Add this to the bottom of books/views.py
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'books/book_detail.html', {'book': book})