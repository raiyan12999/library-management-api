from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta, date

# Create your models here.

class Book(models.Model):

    # Represents books available for borrowing

    title = models.CharField(max_length=100)
    availability = models.BooleanField(default=True) # Is the book available


    def __str__(self):
        return self.title
    

class Borrowed(models.Model):

    # Record for borrowed books and who borrowed them

    user = models.ForeignKey(User, on_delete=models.CASCADE) # user who borrowed the book
    book = models.ForeignKey(Book, on_delete=models.CASCADE) # book that is being borrowed
    borrowing_date = models.DateField(auto_now_add=True) 
    return_deadline = models.DateField()
    returned = models.BooleanField(default=False) # Has the book been returned?

    def calculate_fine(self):

        if date.today() > self.return_deadline:
            overdue_days = (date.today() - self.return_deadline).days
            
            return overdue_days * 5 # Fine of 5 bdt per day
        
        return 0
    
    def __str__(self):
        return f"{self.user.username} - {self.book.title}"

    