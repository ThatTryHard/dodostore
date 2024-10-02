from django.urls import path
from main import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'main'

urlpatterns = [
    path('', views.show_main, name='main'),
    path('products/', views.product_list, name='product_list'),
    path('add_product_to_list/', views.add_product_to_list, name='add_product_to_list'),
    path('xml/', views.show_xml, name='show_xml'),
    path('json/', views.show_json, name='show_json'),
    path('xml/<str:id>/', views.show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:id>/', views.show_json_by_id, name='show_json_by_id'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('edit-product-info/<uuid:id>', views.edit_product_info, name='edit_product_info'),
    path('delete/<uuid:id>', views.delete_product, name='delete_product'),
    path('toggle-theme/', views.toggle_theme, name='toggle_theme'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)