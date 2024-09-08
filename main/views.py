from django.shortcuts import render, redirect
from .models import Product


# Create your views here.
def show_main(request):
    context = {
        'app_name' : 'Dodo Store',
        'name': 'Orlando Devito',
        'class': 'PBP A'
    }

    return render(request, "main.html", context)

def product_list(request):
    # Take all Product data from the database
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})