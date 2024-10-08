from django.shortcuts import render, redirect, reverse, get_object_or_404
from main.models import Product
from main.forms import ProductForm
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core import serializers
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import datetime
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
from django.core.exceptions import ValidationError

@login_required(login_url='/login')
def show_main(request):
    cookies = request.COOKIES
    context = {
        'app_name' : 'Dodo Store',
        'name': request.user.username,
        'class': 'PBP A',
        'last_login' : cookies.get('last_login', 'Not Available'),
    }

    return render(request, "main.html", context)

def product_list(request):
    return render(request, 'product_list.html')

def add_product_to_list(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            add_product = form.save(commit=False)
            add_product.user = request.user
            add_product.save()
            return redirect('main:product_list')
    else:
        form = ProductForm()

    context = {'form': form}
    return render(request, "add_product_to_list.html", context)

def show_xml(request):
    data = Product.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = Product.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("main:main"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            messages.error(request, "Invalid username or password. Please try again.")

    else:
        form = AuthenticationForm(request)
    context = {'form': form}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

def toggle_theme(request):
    if 'theme' in request.session:
        request.session['theme'] = 'light' if request.session['theme'] == 'dark' else 'dark'
    else:
        request.session['theme'] = 'dark'

    return redirect(request.META.get('HTTP_REFERER', '/'))

def is_xss_risky(value):
    return '<' in value or '>' in value

def edit_product_info(request, id):
    product = get_object_or_404(Product, pk=id)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)

    if request.method == "POST":
        post_data = request.POST.copy()
        name = post_data.get('name', '')
        price = post_data.get('price', '')
        description = post_data.get('description', '')
        stock = post_data.get('stock', '')
        category = post_data.get('category', '')

        if any(is_xss_risky(value) for value in [name, description, category]):
            form.add_error(None, "Potential XSS detected in product fields. Please avoid using HTML or special characters.")
        else:
            post_data['name'] = strip_tags(name)
            post_data['price'] = strip_tags(price)
            post_data['description'] = strip_tags(description)
            post_data['stock'] = strip_tags(stock)
            post_data['category'] = strip_tags(category)

            form = ProductForm(post_data, request.FILES or None, instance=product)

            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('main:product_list'))

    context = {'form': form, 'product': product}
    return render(request, "edit_product_info.html", context)

def delete_product(request, id):
    product = Product.objects.get(pk = id)
    product.delete()

    return HttpResponseRedirect(reverse('main:product_list'))

@csrf_exempt
@require_POST
def create_ajax(request):
    if request.method == 'POST':
        name = strip_tags(request.POST.get("name"))
        price = strip_tags(request.POST.get("price"))
        description = strip_tags(request.POST.get("description"))
        stock = strip_tags(request.POST.get("stock"))
        category = strip_tags(request.POST.get("category"))
        image = request.FILES.get("image")
        user = request.user

        if name != request.POST['name']:
            return JsonResponse({'error': 'Potential XSS detected in product name.'})
        
        elif price != request.POST['price']:
            return JsonResponse({'error': 'Potential XSS detected in product price.'})
        
        elif description != request.POST['description']:
            return JsonResponse({'error': 'Potential XSS detected in product description.'})
        
        elif stock != request.POST['stock']:
            return JsonResponse({'error': 'Potential XSS detected in product stock.'})
        
        elif category != request.POST['category']:
            return JsonResponse({'error': 'Potential XSS detected in product category.'})
        
        if not all([name, price, description, stock, category]):
            return JsonResponse({'error': 'Please fill in all required fields'}, status=400)

        new_product = Product(
            name=name,
            price=price,
            description=description,
            stock=stock,
            category=category,
            image=image,
            user=user
        )

        new_product.save()

        return JsonResponse({'message': 'Product created successfully!'})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)