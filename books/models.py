from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    total_number_of_pages = models.IntegerField(null=True, blank=True)
    available = models.BooleanField(default=True)
    location = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.title


# Fixed 'models.models' to 'models.Model' right here:
class BorrowRequest(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('RETURNED', 'Returned'),
    ]

    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='borrow_requests')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='borrow_requests')
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')

    def __str__(self):
        return f"{self.user.username} requested {self.book.title} ({self.status})"