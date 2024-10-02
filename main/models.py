import uuid
from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)  #Product name
    price = models.IntegerField()  # Product price
    description = models.TextField()  # Product description

    stock = models.IntegerField(default=0)  # Product in stock
    category = models.CharField(max_length=100, blank=True, null=True)  # Product category
    image = models.ImageField(upload_to='product_images/', blank=True, null=True) # Product image

    def product_info(self):
        return f"{self.name} - Rp. {self.price:,} - {self.stock} is in stock - {self.category} category."