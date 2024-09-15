from django.shortcuts import render, redirect
from main.models import Product
from main.forms import ProductForm
from django.http import HttpResponse
from django.core import serializers


# Create your views here.
def show_main(request):
    product_list = Product.objects.all()

    context = {
        'app_name' : 'Dodo Store',
        'name': 'Orlando Devito',
        'class': 'PBP A',
        'product_list': product_list
    }

    return render(request, "main.html", context)

def product_list(request):
    # Take all Product data from the database
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def add_product_to_list(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('/')

    context = {'form': form}
    return render(request, "add_product_to_list.html", context)

def show_xml(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")