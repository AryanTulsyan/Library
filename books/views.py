from django.shortcuts import render

from django.shortcuts import render
from .models import Book

def home(request):

    query = request.GET.get('q')

    if query:
        books = Book.objects.filter(title__icontains=query)
    else:
        books = Book.objects.all()

    return render(request, 'home.html', {
        'books': books
    })

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Book, BorrowRequest

def book_list(request):
    books = Book.objects.all()
    return render(request, 'books/book_list.html', {'books': books})

@login_required
def request_borrow(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    already_requested = BorrowRequest.objects.filter(book=book, user=request.user, status__in=['PENDING', 'APPROVED']).exists()
    
    if already_requested:
        messages.warning(request, f"You have already submitted an active request for '{book.title}'.")
    else:
        BorrowRequest.objects.create(book=book, user=request.user)
        messages.success(request, f"Your request to borrow '{book.title}' has been sent to the admin!")
        
    return redirect('book_list')