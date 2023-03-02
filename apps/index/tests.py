from http import HTTPStatus
from http.client import HTTPResponse

from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse

from apps.products.models import Product, ProductCategory, Brand


class IndexTestCase(TestCase):
    def setUp(self) -> None:
        ProductCategory.objects.create(category='Смартфоны')
        Brand.objects.create(name='Google')

        self.brand = Brand.objects.last()
        self.product_category = ProductCategory.objects.last()

        Product.objects.create(
            brand=self.brand,
            category=self.product_category,
            name='Pixel 6a',
            description='Описание смартфона',
            real_price=10000,
            discount=10,
            rating=4.5,
            quantity=5,
            count_sales=10, )

        self.product = Product.objects.last()

    def test_html(self):
        index_url = reverse('index:index')
        response = self.client.get(index_url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.request['REQUEST_METHOD'], 'GET')
        self.assertEqual(response.template_name, ['index/index.html'])

    def test_category(self):
        self.assertEqual(str(self.product_category), 'Смартфоны')
        self.assertEqual(self.product_category.category, 'Смартфоны')
        self.assertEqual(len(ProductCategory.objects.all()), 1)

    def test_brand(self):
        self.assertEqual(str(self.brand), 'Google')
        self.assertEqual(self.brand.name, 'Google')
        self.assertEqual(len(Brand.objects.all()), 1)

    def test_product(self):
        self.assertEqual(self.product.name, 'Pixel 6a')
        self.assertEqual(len(Product.objects.all()), 1)

        discount_price = self.product.real_price - (self.product.real_price // 100 * self.product.discount)
        self.assertEqual(self.product.real_price, 10000)
        self.assertEqual(self.product.discount, 10)
        self.assertEqual(self.product.price, discount_price)

        full_name = 'Google Pixel 6a'
        self.assertEqual(self.product.get_full_name(), full_name)
        self.assertEqual(str(self.product), full_name)
