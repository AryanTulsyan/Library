from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Book, BorrowRequest

def borrow_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    already_borrowed = BorrowRequest.objects.filter(
        book=book, 
        user=request.user, 
        status='APPROVED'
    ).exists()
    
    if already_borrowed:
        messages.error(request, "You have already borrowed this book!")
        return redirect('book_detail', book_id=book.id)
    

    BorrowRequest.objects.create(
        book=book,
        user=request.user,
        status='PENDING'
    )
    
    messages.success(request, "Your borrow request has been submitted for approval!")
    return redirect('book_detail', book_id=book.id)