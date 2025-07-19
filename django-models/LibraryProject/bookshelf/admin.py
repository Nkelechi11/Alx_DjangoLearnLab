from django.contrib import admin
from .models import Book

# Register your models here.
@admin.register(Book)

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')  # Shows these fields in list view
    list_filter = ('author', 'publication_year')            # Adds sidebar filters
    search_fields = ('title', 'author')                     # Enables search by title or author

# admin.site.register(Book, BookAdmin)