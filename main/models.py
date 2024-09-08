from django.db import models
    
class Product(models.Model):
    name = models.CharField(max_length=255)  #Product name
    price = models.IntegerField()  # Product price
    description = models.TextField()  # Product description

    stock = models.IntegerField(default=0)  # Product in stock
    category = models.CharField(max_length=100, blank=True, null=True)  # Product category

    def product_info(self):
        return f"{self.name} - Rp. {self.price:,} - {self.stock} is in stock - {self.category} category."