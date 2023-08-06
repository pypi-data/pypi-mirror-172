import unittest
import base64
import datetime
import lantools

crypt = lantools.crypt

class TestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_1(self):
        self.assertEqual(crypt.encrypt("Hello World"), 'SGVsbG8gV29ybGQ=')

        self.assertEqual(crypt.decrypt('SGVsbG8gV29ybGQ='), "Hello World")

    