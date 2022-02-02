from importlib import import_module
from unittest import skip
from django.conf import settings

from django.contrib.auth.models import User
from django.http import HttpRequest, request
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse

from store.models import Category, Product
from store.views import product_all

# skip is used to skip a test



# Client is a python class that acts as a dummy Web Browser, allowing you tio let your views and interact with Django-powered application programatically.

class TestViewResponses(TestCase):
    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()
        User.objects.create(username='admin')
        Category.objects.create(name='django',slug='django')
        Product.objects.create(category_id=1,title='django beginners',created_by_id=1,
        slug='django-beginners',price='20.00',image='django')
        

    def test_url_allowed_hosts(self):
        """Test Allowed hosts
        """

        response = self.c.get('/')

        self.assertEqual(response.status_code, 200)

    def test_product_detail_url(self):

        response = self.c.get(reverse('store:product_detail', args=['django-beginners']))

        self.assertEqual(response.status_code, 200)

    def test_category_detail_url(self):

        response = self.c.get(reverse('store:category_list', args=['django']))

        self.assertEqual(response.status_code, 200)

    def test_url_allowed_hosts(self):
        """Test Allowed Hosts
        """
        response = self.c.get('/', HTTP_HOST='noaddress.com')
        self.assertEqual(response.status_code, 200)

        response = self.c.get('/', HTTP_HOST='yourdomain.com')
        self.assertEqual(response.status_code, 200)

    def test_product_detail_url(self):
        pass
    
    # def test_homepage_html(self):
    #     request = HttpRequest()

    #     response = product_all(request)

    #     html = response.content.decode('utf8')
        
    #     # to check if title is in the home
    #     self.assertIn('<title>BookStore</title>',html)

    #     # to check whether template starts with DOCTYPE or not
    #     self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))

    #     # to check the response code
    #     self.assertEqual(response.status_code, 200)

        # to know more about advanced testing topics visit /topics/testing/advanced
    
    # def test_view_function(self):
    #     request = self.factory.get('/django-beginners')
    #     response = product_all(request)
    #     html = response.content.decode('utf8')
    #     self.assertIn('<title>BookStore</title>',html)
    #     self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
    #     self.assertEqual(response.status_code, 200)

    def test_homepage_html(self):
        request = HttpRequest()
        engine = import_module(settings.SESSION_ENGINE)
        request.session = engine.SessionStore()
        response = product_all(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>BookStore</title>',html)