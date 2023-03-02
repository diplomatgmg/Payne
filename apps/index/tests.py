from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from apps.products.models import Product, ProductCategory, Brand


class IndexTestCase(TestCase):
    fixtures = ['fixtures/brands.json', 'fixtures/categories.json', 'fixtures/products.json']

    def setUp(self) -> None:
        self.brands = Brand.objects.all()
        self.product_categories = ProductCategory.objects.all()
        self.products = Product.objects.all()

    def test_index(self):
        index_url = reverse('index:index')
        response = self.client.get(index_url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.request['REQUEST_METHOD'], 'GET')
        self.assertTemplateUsed(response, 'index/index.html')

        best_rating_product = self.products.order_by('-rating').first()
        self.assertEqual(response.context_data['best_rating_product'], best_rating_product)

        best_price_products = self.products.order_by('price', '-rating')[:8]
        self.assertEqual(len(response.context_data['best_price_products']), 8)
        self.assertQuerysetEqual(response.context_data['best_price_products'], best_price_products)

        best_rating_products = self.products.order_by('-rating', 'price')[:8]
        self.assertEqual(len(response.context_data['best_rating_products']), 8)
        self.assertQuerysetEqual(response.context_data['best_rating_products'], best_rating_products)

        best_sellers_products = self.products.order_by('-count_sales', 'price')[:4]
        self.assertEqual(len(response.context_data['best_sellers_products']), 4)
        self.assertQuerysetEqual(response.context_data['best_sellers_products'], best_sellers_products)

    def test_category(self):
        self.assertEqual(str(self.product_categories.get(category='Смартфоны')), 'Смартфоны')
        self.assertEqual(len(ProductCategory.objects.all()), 1)

    def test_brand(self):
        self.assertEqual(str(self.brands.get(name='Google')), 'Google')
        self.assertEqual(len(self.brands), 4)

    def test_product(self):
        self.assertEqual(len(self.products), 26)
        product = self.products.get(name='iPhone 13 mini')
        self.assertEqual(product.name, 'iPhone 13 mini')

        discount_price = product.real_price - (product.real_price // 100 * product.discount)
        self.assertEqual(product.real_price, 49000)
        self.assertEqual(product.discount, 47)
        self.assertEqual(product.price, discount_price)

        full_name = 'Apple iPhone 13 mini'
        self.assertEqual(product.get_full_name(), full_name)
        self.assertEqual(str(product), full_name)
