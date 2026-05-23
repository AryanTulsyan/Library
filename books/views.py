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
    """
    Displays the details of a single book.
    """
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'books/book_detail.html', {'book': book})


@login_required
def borrow_book(request, book_id):
    """
    Handles submission of a borrow request for a specific book.
    """
    book = get_object_or_404(Book, id=book_id)
    
    # Check if the current user already has an APPROVED/active request for this exact book
    already_borrowed = BorrowRequest.objects.filter(
        book=book, 
        user=request.user, 
        status='APPROVED'
    ).exists()
    
    if already_borrowed:
        messages.error(request, "You have already borrowed this book!")
        # Safe string path fallback to avoid named-URL mismatch crashes
        return redirect(f'/book/{book.id}/')
    
    # Check if a PENDING request already exists so they don't spam the button
    pending_request = BorrowRequest.objects.filter(
        book=book,
        user=request.user,
        status='PENDING'
    ).exists()

    if pending_request:
        messages.warning(request, "You already have a pending request for this book awaiting approval.")
        return redirect(f'/book/{book.id}/')

    # Create a fresh pending request since no active or pending requests exist
    BorrowRequest.objects.create(
        book=book,
        user=request.user,
        status='PENDING'
    )
    
    messages.success(request, "Your borrow request has been submitted for approval!")
    return redirect(f'/book/{book.id}/')