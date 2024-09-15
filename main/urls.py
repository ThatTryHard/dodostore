from django.urls import path
from main import views

app_name = 'main'

urlpatterns = [
    path('', views.show_main, name='main'),
    path('products/', views.product_list, name='product_list'),\
    path('add_product_to_list/', views.add_product_to_list, name='add_product_to_list'),
    path('xml/', views.show_xml, name='show_xml'),
    path('json/', views.show_json, name='show_json'),
    path('xml/<str:id>/', views.show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:id>/', views.show_json_by_id, name='show_json_by_id'),
]