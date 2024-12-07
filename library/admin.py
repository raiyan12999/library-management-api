from django.contrib import admin
from . models import Book, Borrowed

# Register your models here.

admin.site.register(Borrowed)
admin.site.register(Book)
