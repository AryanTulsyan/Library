from django.contrib import admin

from django.contrib import admin
from .models import Book

admin.site.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('book_name', 'author_name', 'quantity')
    search_fields = ('book_name', 'author_name')