from django.contrib import admin
from .models import Book, BorrowRequest

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # Fixed field names to match your models.py attributes
    list_display = ('title', 'author', 'available', 'location')
    search_fields = ('title', 'author')


@admin.register(BorrowRequest)
class BorrowRequestAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'request_date', 'status')
    list_filter = ('status', 'request_date')
    search_fields = ('book__title', 'user__username')
    actions = ['approve_requests', 'reject_requests']

    def approve_requests(self, request, queryset):
        for borrow_req in queryset:
            # Safely mark the book as unavailable when approved
            borrow_req.book.available = False
            borrow_req.book.save()
        queryset.update(status='APPROVED')
    approve_requests.short_description = "Approve selected borrow requests"

    def reject_requests(self, request, queryset):
        for borrow_req in queryset:
            # Put the book back up for grabs if rejected
            borrow_req.book.available = True
            borrow_req.book.save()
        queryset.update(status='REJECTED')
    reject_requests.short_description = "Reject selected borrow requests"