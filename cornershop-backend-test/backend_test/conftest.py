import os

from django.test import TestCase, TransactionTestCase

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend_test.settings")

TestCase.databases = ["default"]
TransactionTestCase.databases = ["default"]
