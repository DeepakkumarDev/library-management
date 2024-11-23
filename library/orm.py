from django.shortcuts import render
from .models import Book
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

def home(request):
    queryset = ''
    return render(request,"index.html",{'name':'name','books':list(queryset)})





















class ORM:
    pass

    queryset = Book.objects.filter(unit_price__gte=10)
    queryset = Book.objects.filter(unit_price__range=(10,15))
    queryset = Book.objects.filter(collection__id__range=(1,3))
    queryset = Book.objects.filter(title__icontains='the')
    queryset = Book.objects.filter(title__istartswith='the')
    queryset = Book.objects.filter(description__isnull=True)

    # queryset = Book.objects.all()
    # for book in queryset:
    #     print(book)
    # book = Book.objects.get(pk=1)

    # try:
    #     book = Book.objects.get(pk=0)
    # except ObjectDoesNotExist:
    #     pass

    # book = Book.objects.filter(pk=0).first()
    # exist = Book.objects.filter(pk=0).exists()