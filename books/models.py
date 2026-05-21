from django.db import models

from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    total_number_of_pages = models.IntegerField(null=True, blank=True)
    available = models.BooleanField(default=True)
    location = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.title
