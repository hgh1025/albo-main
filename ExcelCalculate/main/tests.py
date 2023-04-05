from django.test import TestCase
from main.models import Product

class ProductModelTest(TestCase):
    def test_create_product(self):
        product = Product.objects.create(name='test', description='test description', price=10000, stock=10)
        self.assertEqual(product.name, 'test')
        self.assertEqual(product.description, 'test 11')
        self.assertEqual(product.price, 10000)
        self.assertEqual(product.stock, 10)
    
    def test_update_product(self):
        product = Product.objects.create(name='test', description='test description', price=10000, stock=10)
        product.name = 'new test'
        product.description = 'new test description'
        product.price = 20000
        product.stock = 5
        product.save()
        product.refresh_from_db()
        self.assertEqual(product.name, 'new test')
        self.assertEqual(product.description, 'new test description')
        self.assertEqual(product.price, 20000)
        self.assertEqual(product.stock, 5)
    
    def test_delete_product(self):
        product = Product.objects.create(name='test', description='test description', price=10000, stock=10)
        product.delete()
        self.assertEqual(Product.objects.count(), 0)
