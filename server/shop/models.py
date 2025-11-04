from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now
User = get_user_model()
class Product(models.Model):
    name = models.CharField(max_length=200)
    price_cents = models.PositiveIntegerField()
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=now)
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=now)
    total_cents = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, default="pending")
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    line_total_cents = models.PositiveIntegerField(default=0)
class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="payment")
    provider = models.CharField(max_length=20, default="mock")
    provider_ref = models.CharField(max_length=120, blank=True)
    amount_cents = models.PositiveIntegerField()
    status = models.CharField(max_length=20, default="initiated")
    created_at = models.DateTimeField(default=now)
