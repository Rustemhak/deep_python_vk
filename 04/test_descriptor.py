import unittest
from descriptor import Product


class TestDescriptor(unittest.TestCase):
    def test_creation(self):
        test_product = Product('sweet', 5, 0.1)

        self.assertEqual(test_product.weight, 0.1)
        self.assertEqual(test_product.name, 'sweet')
        self.assertEqual(test_product.price, 5)

    def test_num(self):
        with self.assertRaises(TypeError):
            Product('test', 1.2, 9.2)
        with self.assertRaises(TypeError):
            Product('test', '', 3)

    def test_name(self):
        with self.assertRaises(TypeError):
            Product(0, 0, 0)
        with self.assertRaises(TypeError):
            Product(0, 8.9, 0)

    def test_price(self):
        with self.assertRaises(TypeError):
            Product('test', 9.9, 0)
        with self.assertRaises(ValueError):
            Product('test', -1, 0)

    def test_change_val(self):
        test_product = Product('test', 1, 0.1)

        test_product.weight = 4.2
        self.assertEqual(test_product.weight, 4.2)
        with self.assertRaises(TypeError):
            test_product.weight = 'test'
        with self.assertRaises(TypeError):
            test_product.weight = 4
        self.assertEqual(test_product.weight, 4.2)

        test_product.name = 'test'
        self.assertEqual(test_product.name, 'test')
        with self.assertRaises(TypeError):
            test_product.name = -1
        self.assertEqual(test_product.name, 'test')

        test_product.price = 25
        self.assertEqual(test_product.price, 25)
        with self.assertRaises(ValueError):
            test_product.price = -1
        self.assertEqual(test_product.price, 25)
