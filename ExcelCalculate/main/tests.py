from django.test import TestCase
from main.models import Item

class ProductModelTest(TestCase):
    def test_create_product(self):
        product = Item.objects.create(item_name='test', item_content='test description', item_price =10000, stock=10)
        self.assertEqual(product.item_name, 'test')
        self.assertEqual(product.item_content, 'test 11')
        self.assertEqual(product.item_price , 10000)
        self.assertEqual(product.stock, 10)
    
    def test_update_product(self):
        product = Item.objects.create(item_name='test', item_content='test description', item_price =10000, stock=10)
        product.item_name = 'new test'
        product.item_content = 'new test description'
        product.item_price  = 20000
        product.stock = 5
        product.save()
        product.refresh_from_db()
        self.assertEqual(product.item_name, 'new test')
        self.assertEqual(product.item_content, 'new test description')
        self.assertEqual(product.item_price , 20000)
        self.assertEqual(product.stock, 5)
    
    def test_delete_product(self):
        product = Item.objects.create(item_name='test', item_content='test description', item_price =10000, stock=10)
        product.delete()
        self.assertEqual(Product.objects.count(), 0)
