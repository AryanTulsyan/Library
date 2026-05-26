from django.contrib import admin
from .models import Book, BorrowRequest

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # 🌟 REMOVED: 'total_number_of_pages' is no longer listed in the main columns
    list_display = ['call_number', 'title', 'author', 'deposit_fee', 'borrow_fee', 'available']
    
    list_display_links = ['title']
    list_editable = ['call_number', 'available']
    search_fields = ['title', 'author', 'call_number']
    
    # 🌟 EXCLUDED: Hides deposit_fee from the "Add Book" / "Edit Book" forms 
    # so it automatically uses the constant 500.00 fallback value instead
    exclude = ['deposit_fee']

@admin.register(BorrowRequest)
class BorrowRequestAdmin(admin.ModelAdmin):
    list_display = ['book', 'borrower_name', 'borrower_phone', 'status', 'delivery_location', 'requested_at']
    list_filter = ['status']
    actions = ['approve_requests', 'mark_returned']

    def approve_requests(self, request, queryset):
        for req in queryset:
            req.status = 'APPROVED'
            req.save()
            req.book.available = False
            req.book.save()
    approve_requests.short_description = "Approve selected requests (Mark Books Out)"

    def mark_returned(self, request, queryset):
        for req in queryset:
            req.status = 'RETURNED'
            req.save()
            req.book.available = True
            req.book.save()
    mark_returned.short_description = "Mark selected requests as Returned (Restock Books)"