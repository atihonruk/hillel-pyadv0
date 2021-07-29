from django.contrib import admin

from .models import Author, Book

class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'isbn', 'category')
    list_display_links = ('title',)
    list_filter = ('category',)
    ordering = ('title',)
    search_fields = ('title',) # title like '%term%'
    readonly_fields = ('slug',)

admin.site.register(Author)
admin.site.register(Book, BookAdmin)

