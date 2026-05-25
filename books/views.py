from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Book, BorrowRequest

def book_list(request):
    query = request.GET.get('q')
    if query:
        books = Book.objects.filter(title__icontains=query) | Book.objects.filter(author__icontains=query)
    else:
        books = Book.objects.all()
    return render(request, 'books/book_list.html', {'books': books})

# 🌟 LOOK: No @login_required here anymore! Anyone can access this view.
def request_borrow(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    if not book.available:
        messages.error(request, f"Sorry, '{book.title}' is currently checked out!")
        return redirect('book_list')

    if request.method == 'POST':
        user_location = request.POST.get('delivery_location', '').strip()
        guest_name = request.POST.get('borrower_name', '').strip()
        guest_phone = request.POST.get('borrower_phone', '').strip()
        
        calculated_delivery = 2.50 if user_location and user_location.lower() != "library pick-up" else 0.00

        # Check for duplicates using name/phone for guests, or user profiles for members
        if request.user.is_authenticated:
            already_requested = BorrowRequest.objects.filter(user=request.user, book=book, status='PENDING').exists()
        else:
            already_requested = BorrowRequest.objects.filter(borrower_phone=guest_phone, book=book, status='PENDING').exists()

        if already_requested:
            messages.warning(request, "A pending request for this book under these details already exists.")
            return redirect('book_list')

        # Create the request record safely
        BorrowRequest.objects.create(
            book=book,
            user=request.user if request.user.is_authenticated else None, # Link profile if member
            borrower_name=guest_name if not request.user.is_authenticated else None,
            borrower_phone=guest_phone if not request.user.is_authenticated else None,
            status='PENDING',
            delivery_location=user_location if user_location else "Main Library Pick-up",
            delivery_charge=calculated_delivery
        )
        
        messages.success(request, f"Success! Request submitted. Send your deposit payment to complete the order.")
        return redirect('book_list')

    return redirect('book_list')