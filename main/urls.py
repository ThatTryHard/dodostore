from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.show_main, name='main'),
    path('products/', views.product_list, name='product_list'),
]