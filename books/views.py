from django.shortcuts import render

from django.shortcuts import render
from .models import Book

def home(request):

    query = request.GET.get('q')

    if query:
        books = Book.objects.filter(title__icontains=query)
    else:
        books = Book.objects.all()

    return render(request, 'home.html', {
        'books': books
    })
