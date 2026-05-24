from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Book, BorrowRequest

def book_list(request):
    """
    Displays all books in the library.
    """
    books = Book.objects.all()
    return render(request, 'books/book_list.html', {'books': books})


def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'books/book_list.html', {'book': book})

@login_required
def request_borrow(request, book_id):
    """
    Handles submission of a borrow request for a specific book.
    """
    book = get_object_or_404(Book, id=book_id)
    
    try:
        # Use user_id directly to guarantee clean execution on the database level
        already_borrowed = BorrowRequest.objects.filter(
            book_id=book.id, 
            user_id=request.user.id, 
            status='APPROVED'
        ).exists()
        
        if already_borrowed:
            messages.error(request, "You have already borrowed this book!")
            return redirect(f'/book/{book.id}/')
        
        pending_request = BorrowRequest.objects.filter(
            book_id=book.id,
            user_id=request.user.id,
            status='PENDING'
        ).exists()

        if pending_request:
            messages.warning(request, "You already have a pending request for this book awaiting approval.")
            return redirect(f'/book/{book.id}/')

        # Create a fresh pending request
        BorrowRequest.objects.create(
            book=book,
            user=request.user,
            status='PENDING'
        )
        messages.success(request, "Your borrow request has been submitted for approval!")
        
    except Exception as e:
        # If any internal DB or matching error happens, intercept it gracefully 
        # instead of letting the server function throw a 500 crash
        messages.error(request, "An internal error occurred while processing your request. Please try again.")
        
    return redirect(f'/book/{book.id}/')