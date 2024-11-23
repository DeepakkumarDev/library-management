from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from uuid import uuid4
from django.conf import settings
from .validators import validate_file_size

# Collection model: Represents a collection of books
class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_book = models.ForeignKey(
        'Book',
        on_delete=models.SET_NULL,
        null=True,
        related_name='+'
    )

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['title']


# Book model: Represents individual books in the system
class Book(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    author = models.CharField(max_length=255)
    unit_price = models.DecimalField(max_digits=6,decimal_places=2)
    description = models.TextField()
    available = models.BooleanField(default=True)
    stock = models.PositiveSmallIntegerField()
    collection = models.ForeignKey(
        Collection,
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['title']


# BookImage model: Stores images related to books
class BookImage(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='books/images',
        validators=[
            validate_file_size,
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])
        ]
    )


# Borrower model: Represents users who borrow books
class Borrower(models.Model):
    phone = models.CharField(max_length=15)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


    def first_name(self):
        return self.user.first_name

    def last_name(self):
        return self.user.last_name

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


# Loan model: Keeps track of borrowed books
class Loan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"Loan: {self.book.title} to {self.borrower}"


# Address model: Stores borrower's addresses
class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.street}, {self.city}"


# Cart model: Represents a shopping cart (for borrowing/purchasing books)
class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


# CartItem model: Represents items in a cart
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(3)]
    )

    def __str__(self):
        return f"{self.quantity} of {self.book.title}"

