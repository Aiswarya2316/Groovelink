from django.db import models

# Create your models here.
# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
    is_shop_owner = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # You can adjust the max_length based on your needs
    location = models.CharField(max_length=255, blank=True, null=True)  # You can adjust the max_length as well

    def __str__(self):
        return self.username

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    shop_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    total_quantity = models.PositiveIntegerField(default=1)  # Total items in inventory
    available_quantity = models.PositiveIntegerField(default=1)  # Currently available items
    dimensions = models.CharField(max_length=200, blank=True, null=True)  # New field for dimensions
    installation_instructions = models.TextField(blank=True, null=True)  # New field for installation instructions
    compatibility = models.TextField(blank=True, null=True)  # New field for compatibility
    power_rating = models.CharField(max_length=100, blank=True, null=True)  # New field for power rating
    pincode = models.CharField(max_length=6, blank=True, null=True, default='683511')  # Default pincode for old records

    def average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            return sum(review.rating for review in reviews) / len(reviews)
        return 0
    def __str__(self):
        return self.name

    def update_availability(self):
        self.is_available = self.available_quantity > 0
        self.save()

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    returned = models.BooleanField(default=False)
    return_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
    

class Review(models.Model):
    RATING_CHOICES = (
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    )
    
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
