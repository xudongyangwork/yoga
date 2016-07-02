# -*- coding:utf-8 -*-
from django.test import TestCase

__author__ = 'xdy'


class DemoTestCase(TestCase):
    def setUp(self):
        pass

    def test_demo(self):
        """python manage.py test main_site.testing.test_demo.DemoTestCase.first_test"""

        self.assertEqual(1, 1)
