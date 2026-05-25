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

def request_borrow(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    if not book.available:
        messages.error(request, f"Sorry, '{book.title}' is currently checked out!")
        return redirect('book_list')

    if request.method == 'POST':
        selected_zone = request.POST.get('delivery_location', '').strip()
        guest_name = request.POST.get('borrower_name', '').strip()
        guest_phone = request.POST.get('borrower_phone', '').strip()
        
        # 🌟 Map selected choices straight to backend financial database metrics
        zone_pricing = {
            "Library Pick-up": 0.00,
            "Local Courier (Within 5km)": 40.00,
            "City Delivery (5-15km)": 90.00,
            "Out of City Shipping": 150.00
        }
        calculated_delivery = zone_pricing.get(selected_zone, 0.00)

        # Check for duplicates using member account profiles or contact metrics
        if request.user.is_authenticated:
            already_requested = BorrowRequest.objects.filter(user=request.user, book=book, status='PENDING').exists()
        else:
            already_requested = BorrowRequest.objects.filter(borrower_phone=guest_phone, book=book, status='PENDING').exists()

        if already_requested:
            messages.warning(request, "A pending request for this book under these details already exists.")
            return redirect('book_list')

        # Instantiate secure database record mapping variables cleanly
        BorrowRequest.objects.create(
            book=book,
            user=request.user if request.user.is_authenticated else None,
            borrower_name=guest_name if not request.user.is_authenticated else None,
            borrower_phone=guest_phone if not request.user.is_authenticated else None,
            status='PENDING',
            delivery_location=selected_zone,
            delivery_charge=calculated_delivery
        )
        
        total_due = book.deposit_fee + calculated_delivery
        messages.success(request, f"Success! Request submitted. Please transfer ₹{total_due:.2f} to complete your order.")
        return redirect('book_list')

    return redirect('book_list')

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'books/book_detail.html', {'book': book})

def about_page(request):
    return render(request, 'books/about.html')