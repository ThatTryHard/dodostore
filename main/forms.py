from django.forms import ModelForm
from main.models import Product
from django.utils.html import strip_tags

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price", "description", "stock", "category", "image"]

    def clean_mood(self):
        name = self.cleaned_data["name"]
        return strip_tags(name)

    def clean_price(self):
        price = self.cleaned_data["price"]
        return strip_tags(price)
    
    def clean_description(self):
        description = self.cleaned_data["description"]
        return strip_tags(description)
    
    def clean_stock(self):
        stock = self.cleaned_data["stock"]
        return strip_tags(stock)

    def clean_category(self):
        category = self.cleaned_data["category"]
        return strip_tags(category)