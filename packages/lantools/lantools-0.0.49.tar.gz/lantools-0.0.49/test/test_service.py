import unittest
from lantools import service

class App(service.Service):
    def __init__(self):
        super().__init__()
        self.counter = 0
    
    def _mysql(self):
        self.counter = self.counter + 1
        return "mysql"+ str(self.counter)

    def _logger(self):
        raise Exception("xxx")


class TestCase(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass

    def test_1(self):
        app = App()

        self.assertEqual(app.mysql, 'mysql1')
        self.assertEqual(app.mysql, 'mysql1')

    def test_2(self):
        app = App()

        self.assertEqual(app.redis, None)

    def test_3(self):
        app = App()

        with self.assertRaises(Exception) as e:
            app.logger

        self.assertEqual(str(e.exception), 'xxx')


