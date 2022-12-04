from .utils import generate_key
from .models import Url
from django.db import IntegrityError
from django.test import TestCase
from django.test import Client
from django import setup
import os
import json


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'url_shortner_api.settings')
setup()


# Create your tests here.
class CreateUrlTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.base_url = '/create'

    def test_create_new_url(self):
        data = {"url": "https://ravkavonline.co.il"}
        res = self.client.post(
            self.base_url, data, content_type='application/json')
        res_data = res.json()
        self.assertEqual(res.status_code, 201)
        self.assertTrue('id' in res_data)
        self.assertTrue('url' in res_data and res_data['url'] == data['url'])
        self.assertTrue('key' in res_data)
        self.assertTrue(
            'redirects_count' in res_data and res_data['redirects_count'] == 0)

    def test_add_invalid_url(self):
        data = {"url": "abc"}
        res = self.client.post(
            self.base_url, data, content_type='application/json')
        self.assertEqual(res.status_code, 400)

    def test_request_without_data(self):
        res = self.client.post(self.base_url, content_type='application/json')
        self.assertEqual(res.status_code, 400)

    def test_not_post_request(self):
        res = self.client.get(self.base_url)
        self.assertEqual(res.status_code, 404)

    def test_error_creating_key(self):
        with self.settings(URL_KEY_LENGTH=0):
            data = {"url": "https://ravkavonline.co.il"}
            res = self.client.post(
                self.base_url, data, content_type='application/json')
            self.assertEqual(res.status_code, 500)

    def test_unique_key(self):
        url = 'https://ravkavonline.co.il'
        key = generate_key()
        Url(url=url, key=key).save()

        with self.assertRaises(IntegrityError):
            url = 'ynet.co.il'
            Url(url=url, key=key).save()


class RedirectUrlTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        key = generate_key(7)
        new_url = Url(url='ynet.co.il', key=key)
        new_url.save()
        self.valid_url = new_url

    def test_redirect(self):
        key = self.valid_url.key
        path = f'/s/{key}'
        res = self.client.get(path)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, self.valid_url.url)

    def test_key_not_exist(self):
        key = 'a'  # key shorter than in db
        path = f'/s/{key}'
        res = self.client.get(path)
        self.assertEqual(res.status_code, 400)
