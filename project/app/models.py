from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.PositiveBigIntegerField()
    password = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Staf(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class AdminReg(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.PositiveBigIntegerField()
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.name

from django.db import models

class BandTeam(models.Model):
    staf = models.ForeignKey(Staf, on_delete=models.CASCADE, related_name="bands")
    name = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    description = models.TextField()
    booking_fee = models.IntegerField(default=0)  # Added a default value to prevent NULL errors
    image = models.ImageField(upload_to="bands/")

    def __str__(self):
        return self.name


class Product(models.Model):
    staf = models.ForeignKey(Staf, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to="products/")

    def __str__(self):
        return self.name


    
    from django.db import models

class Booking(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="bookings", null=True, blank=True)
    band = models.ForeignKey(BandTeam, on_delete=models.CASCADE, related_name="bookings")
    event_date = models.DateField()
    status = models.CharField(
        max_length=20, 
        choices=[("Pending", "Pending"), ("Confirmed", "Confirmed")], 
        default="Pending"
    )
    payment_id = models.CharField(max_length=100, blank=True, null=True)  # Store Razorpay payment ID
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.band.name} booked on {self.event_date} by {self.customer.email}"




# ✅ Order model updated for Pay Later feature
class Order(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE, related_name="orders")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="orders")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.BooleanField(default=False)  # False means unpaid
    order_status = models.CharField(
        max_length=20,
        choices=[("Pending", "Pending"), ("Processing", "Processing"), ("Delivered", "Delivered")],
        default="Pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer.name}"




