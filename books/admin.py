from django.contrib import admin
from .models import Book, BorrowRequest

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'available', 'borrow_fee_percentage', 'deposit_fee')
    search_fields = ('title', 'author')

@admin.register(BorrowRequest)
class BorrowRequestAdmin(admin.ModelAdmin):
    # Displays either the club username or guest name depending on who ordered
    list_display = ('book', 'get_borrower', 'status', 'delivery_location', 'delivery_charge', 'request_date')
    list_filter = ('status', 'request_date')
    search_fields = ('book__title', 'user__username', 'borrower_name', 'borrower_phone')
    actions = ['approve_requests', 'reject_requests', 'mark_as_returned']

    def get_borrower(self, obj):
        if obj.user:
            return f"🌟 Member: {obj.user.username}"
        return f"👤 Guest: {obj.borrower_name} ({obj.borrower_phone})"
    get_borrower.short_description = 'Borrower Details'
    
    # ... leave your action functions below exactly as they are ...
    def approve_requests(self, request, queryset):
        # Update the request status
        queryset.update(status='APPROVED')
        
        # Automatically mark the corresponding books as unavailable
        for borrow_req in queryset:
            borrow_req.book.available = False
            borrow_req.book.save()
            
        self.message_user(request, "Selected requests have been APPROVED and books marked as unavailable.")
    approve_requests.short_description = "✅ Approve selected borrow requests"

    def reject_requests(self, request, queryset):
        queryset.update(status='REJECTED')
        self.message_user(request, "Selected requests have been REJECTED.")
    reject_requests.short_description = "❌ Reject selected borrow requests"

    def mark_as_returned(self, request, queryset):
        queryset.update(status='RETURNED')
        
        # Make the books available again for the next reader
        for borrow_req in queryset:
            borrow_req.book.available = True
            borrow_req.book.save()
            
        self.message_user(request, "Selected requests marked as RETURNED and books are back in stock.")
    mark_as_returned.short_description = "🔄 Mark books as safely returned"