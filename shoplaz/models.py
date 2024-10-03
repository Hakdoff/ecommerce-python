from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    category_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.category_name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_id = models.CharField(max_length=100, blank=True)
    product_name = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    size = models.CharField(max_length=250, blank=True)
    price = models.FloatField()
    stock = models.PositiveIntegerField()
    images = models.ImageField(default='fallback.png', blank=True)

    def __str__(self):
        return self.product_name


class Cart(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product_id.product_name} - {self.quantity} pcs"
