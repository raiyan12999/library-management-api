from rest_framework import serializers
from .models import Book, Borrowed
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    # serializer for user model, converts objects to JSON and vice versa

    class Meta:
        model = User
        fields = ['id', 'username', 'is_staff']

class BookSerializer(serializers.ModelSerializer):

    # for Book model

    class Meta:
        model = Book
        fields = ['id', 'title', 'availability']

class BorrowedSerializer(serializers.ModelSerializer):

    # serializer for Borrowed model

    book = BookSerializer(read_only = True) #Embed book details
    user = UserSerializer(read_only = True) 

    class Meta:
        model = Borrowed
        fields = ['id', 'user', 'book', 'borrowing_date', 'return_deadline', 'returned']

        
