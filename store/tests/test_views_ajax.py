from unicodedata import category
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from store.models import Category, Product

class TestBasketView(TestCase):

    def setUp(self) -> None:
        User.objects.create(username='admin')
        
        Category.objects.create(name='django',slug='django')
        
        Product.objects.create(category_id=1,title='django-beginners',created_by_id=1,
        slug='django-beginners',price='20',image='django')

        Product.objects.create(category_id=1,title='django-intermediate',created_by_id=1,
        slug='django-intermediate',price='30',image='django')

        Product.objects.create(category_id=1,title='django-advanced',created_by_id=1,
        slug='django-advanced',price='50',image='django')

        self.client.post(
            reverse('basket:basket_add') , 
            {"productid":1,"productqty":1,"action":"post"}
        )

        self.client.post(
            reverse('basket:basket_add') , 
            {"productid":2,"productqty":2,"action":"post"}
        )

    
    def test_basket_url(self):
        """
        Test homepage response status
        """
        response = self.client.get(reverse('basket:basket_summary'))

        self.assertEqual(response.status_code, 200)

    
    def test_basket_add(self):
        """
        Test adding items to the basket
        """

        response = self.client.post(
            reverse('basket:basket_add'),
            {"productid":3,"productqty":1,"action":"post"},
            xhr=True
        )

        self.assertEqual(response.json(),{'qty':4})

        response = self.client.post(
            reverse('basket:basket_add'),
            {"productid":2,"productqty":1,"action":"post"},
            xhr=True
        )

        self.assertEqual(response.json(),{'qty':3})

    def test_basket_delete(self):
        """
        Test Deleting from the basket
        """
        response = self.client.post(
            reverse('basket:basket_delete'),
            {"productid":2,"action":"post"},
            xhr=True
        )

        self.assertEqual(response.json(),{'status':'deleted successfully','subtotal':'20.00'})

    
    def test_basket_update(self):
        """
        Test updating items from the basket
        """

        response = self.client.post(
            reverse('basket:basket_update'),
            {"productid":2,"productqty":1,"action":"post"},
            xhr=True
            )

        self.assertEqual(response.json(),{'qty':2,'subtotal':'50.00'})