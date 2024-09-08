from django.test import TestCase, Client
from django.utils import timezone
from .models import Product

class mainTest(TestCase):
    def test_main_url_is_exist(self):
        response = Client().get('')
        self.assertEqual(response.status_code, 200)

    def test_main_using_main_template(self):
        response = Client().get('')
        self.assertTemplateUsed(response, 'main.html')

    def test_nonexistent_page(self):
        response = Client().get('/nonexistant/')
        self.assertEqual(response.status_code, 404)

    def test_product_exist(self):
        product = Product.objects.create(
          name="Aqua",
          price = 4000,
          description = "a bottle of drinking water from the Aqua brand",
          stock = 1000,
          category = "Beverage",
        )
        self.assertTrue("Aqua - Rp. 4,000 - 1000 is in stock - Beverage category." == product.product_info())