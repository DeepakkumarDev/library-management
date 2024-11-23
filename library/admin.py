from django.contrib import admin
from . import models 
from django.db.models.aggregates import Count 

# Register your models here.
# admin.site.register(models.Collection)
# admin.site.register(models.Book)


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title','books_count']
    @admin.display(ordering='books_count')
    def books_count(self,collection):
        return collection.books_count 
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            books_count=Count('book')
        )

@admin.register(models.Book)
class BookAdmin(admin.ModelAdmin):
    list_display =['title','author','unit_price','collection_title','stock_status']
    list_select_related = ['collection']
    list_editable = ['unit_price']
    list_per_page = 10 

    def collection_title(self,book):
        return book.collection.title
    
    @admin.display(ordering='stock')
    def stock_status(self,book):
        if book.stock < 5:
            return 'low'
        return 'ok'
        
@admin.register(models.Borrower)
class BorrowerAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone','user__first_name', 'user__last_name']
    list_editable = ['phone']
    ordering = ['user__first_name','user__last_name']
    list_per_page = 10 


@admin.register(models.Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ['book','borrower','borrow_date','return_date','is_returned']
    ordering = ['borrower','is_returned']


@admin.register(models.Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['city','borrower','street']
    ordering = ['borrower']
    list_per_page = 10 
    
