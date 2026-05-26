from django.contrib import admin
from .models import Book, BorrowRequest

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # 1. Keep your column arrangement
    list_display = ['call_number', 'title', 'author', 'deposit_fee', 'borrow_fee', 'available']
    
    # 🌟 2. Explicitly make the 'title' column the clickable link to open the edit page
    list_display_links = ['title']
    
    # 3. Now you can safely edit call numbers and availability right from the main grid!
    list_editable = ['call_number', 'available']
    
    search_fields = ['title', 'author', 'call_number']
@admin.register(BorrowRequest)
class BorrowRequestAdmin(admin.ModelAdmin):
    list_display = ['book', 'borrower_name', 'borrower_phone', 'status', 'delivery_location', 'requested_at']
    list_filter = ['status']
    actions = ['approve_requests', 'mark_returned']

    def approve_requests(self, request, queryset):
        for req in queryset:
            req.status = 'APPROVED'
            req.save()
            # Mark the actual book as unavailable when order goes out
            req.book.available = False
            req.book.save()
    approve_requests.short_description = "Approve selected requests (Mark Books Out)"

    def mark_returned(self, request, queryset):
        for req in queryset:
            req.status = 'RETURNED'
            req.save()
            # Return the book back to active shelf inventory
            req.book.available = True
            req.book.save()
    mark_returned.short_description = "Mark selected requests as Returned (Restock Books)"