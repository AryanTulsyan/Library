from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    total_number_of_pages = models.IntegerField(null=True, blank=True)
    available = models.BooleanField(default=True)
    location = models.CharField(max_length=10, null=True, blank=True)
    borrow_fee_percentage = models.IntegerField(default=10, help_text="Enter fee as a percentage of the deposit")
    deposit_fee = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    payment_number = models.CharField(max_length=50, default=9833770438)
    
    @property
    def total_fee(self):
        return self.borrow_fee + self.deposit_fee

    def __str__(self):
        return self.title


class BorrowRequest(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('RETURNED', 'Returned'),
    ]

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrow_requests')
    
    # 🌟 CHANGED: user is now optional so non-members can borrow
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='borrow_requests')
    
    # 🌟 NEW: Track guest information directly
    borrower_name = models.CharField(max_length=100, null=True, blank=True)
    borrower_phone = models.CharField(max_length=20, null=True, blank=True)
    
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    delivery_location = models.CharField(max_length=255, default="Main Library Pick-up")
    delivery_charge = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    @property
    def total_upfront_due(self):
        return self.book.deposit_fee + self.delivery_charge

    def __str__(self):
        name = self.user.username if self.user else self.borrower_name
        return f"{name} requested {self.book.title} ({self.status})"