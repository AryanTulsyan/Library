from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    total_number_of_pages = models.IntegerField(default=100)
    available = models.BooleanField(default=True)
    deposit_fee = models.DecimalField(max_digits=6, decimal_places=2)
    borrow_fee = models.IntegerField(default=10)  # Handles your Option 2 percentage math
    payment_number = models.CharField(max_length=50, default="9833950030")
    
    # 🌟 Call Number field integrated safely
    call_number = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        help_text="e.g., PR 6056 .I2 Z5 2026"
    )

    class Meta:
        ordering = ['call_number', 'title']

    def __str__(self):
        prefix = self.call_number if self.call_number else "UNCATEGORIZED"
        return f"[{prefix}] {self.title}"


# 🌟 RESTORED: The BorrowRequest model needed by your admin and views
class BorrowRequest(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending Approval'),
        ('APPROVED', 'Approved / Out for Delivery'),
        ('RETURNED', 'Returned / Closed'),
        ('REJECTED', 'Rejected'),
    ]

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrow_requests")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Guest fields for non-logged-in visitors
    borrower_name = models.CharField(max_length=100, null=True, blank=True)
    borrower_phone = models.CharField(max_length=20, null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    delivery_location = models.CharField(max_length=255, default="Self Pick-up from Library")
    delivery_charge = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        name = self.user.username if self.user else (self.borrower_name or "Guest")
        return f"Request by {name} for '{self.book.title}' ({self.status})"