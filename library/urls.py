from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BorrowedViewSet, BookViewSet

router = DefaultRouter()
router.register('books', BookViewSet, basename='books')
router.register('borrowed', BorrowedViewSet, basename='borrowed')

urlpatterns = [
    path('', include(router.urls)),
]