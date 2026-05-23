from django.contrib import admin

from django.contrib import admin
from .models import Book

admin.site.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('book_name', 'author_name', 'quantity')
    search_fields = ('book_name', 'author_name')

from django.contrib import admin
from .models import Book, BorrowRequest

@admin.register(BorrowRequest)
class BorrowRequestAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'request_date', 'status')
    list_filter = ('status', 'request_date')
    search_fields = ('book__title', 'user__username')
    actions = ['approve_requests', 'reject_requests']

    def approve_requests(self, request, queryset):
        queryset.update(status='APPROVED')
    approve_requests.short_description = "Approve selected borrow requests"

    def reject_requests(self, request, queryset):
        queryset.update(status='REJECTED')
    reject_requests.short_description = "Reject selected borrow requests"