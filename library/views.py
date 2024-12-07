# Create your views here.
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db import transaction
from . models import Book, Borrowed
from . serializers import UserSerializer, BookSerializer, BorrowedSerializer
from datetime import timedelta, date


class CustomPagination(PageNumberPagination):

    # custom pagination for controlling page size and limits

    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 20

class BookViewSet(viewsets.ModelViewSet):

    # ViewSet for managing books
    # Admins: Full CRUD access
    # Users: Read only access

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = CustomPagination

    def get_permissions(self):

        # For setting permissions
        # Admin full CRUD
        # Users Read-only

        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        
        return [IsAuthenticated()]
    

class BorrowedViewSet(viewsets.ModelViewSet):

    # Viewset for managing borrowed items
    # User can borrow and return book

    queryset = Borrowed.objects.all()
    serializer_class = BorrowedSerializer


    def get_queryset(self):

        # Limit borrowing records to the logged-in user

        if not self.request.user.is_staff:
            return self.queryset # Admins can see all the records
        return self.queryset.filter(user=self.request.user) #Filter  by user
    
    @action(detail=True, methods=['post'])
    def borrow(self, request, pk=None):

        # custom action to borrow a 


        try:
            book = Book.objects.get(pk = pk)
        except Book.DoesNotExist:
            return Response({'error': 'Book not found.'}, status=404)


        if not book.availability:
            return Response ({'error' : 'Book is not available for rent.'}, status = 400)
        
        if Borrowed.objects.filter(user=request.user, returned=False).count() >= 5:
            return Response({'error': 'Borrow limit reached!'}, status=400)

        # Enforce concurrency 
        with transaction.atomic():
            book.availability = False
            book.save()

            borrow = Borrowed.objects.create(
                user = request.user,
                book = book,
                return_deadline = date.today() + timedelta(days=14)
            )


    @action(detail=True, methods=['post'])
    def return_book(self, request, pk = None):
        # Custom action to return a book

        try:
            borrow = Borrowed.objects.get(book_id=pk, user=request.user, returned=False)
        except Borrowed.DoesNotExist:
            return Response({'error': 'No active borrowing record found for this book.'}, status=404)



        borrow.returned = True
        borrow.save()

        book = borrow.book
        book.availability = True
        book.save()

        fine = borrow.calculate_fine()

        return Response({'message' : f'Book "{book.title}" returned successfully.', 'fine': fine})