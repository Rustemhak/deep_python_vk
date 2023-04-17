import unittest
from custom_list import CustomList


class TestClass(unittest.TestCase):
    def test_operations(self):
        cl_a = CustomList([5, 1, 3, 7])
        cl_b = CustomList([1, 2, 7])
        cl_c = cl_a - cl_b
        self.assertListEqual(list(cl_c), [4, -1, -4, 7])
        self.assertListEqual(list(cl_a), [5, 1, 3, 7])
        self.assertListEqual(list(cl_b), [1, 2, 7])

        cl_a = CustomList([5, 1, 3, 7])
        cl_b = CustomList([1, 2, 7])
        cl_c = cl_a + cl_b
        self.assertListEqual(list(cl_c), [6, 3, 10, 7])
        self.assertListEqual(list(cl_a), [5, 1, 3, 7])
        self.assertListEqual(list(cl_b), [1, 2, 7])

        l_a = [1, 2]
        cl_b = CustomList([3, 4])
        cl_c = l_a + cl_b
        self.assertListEqual(list(cl_c), [4, 6])

        l_a = [1, 2]
        cl_b = CustomList([3, 4])
        cl_c = l_a - cl_b
        self.assertListEqual(list(cl_c), [-2, -2])

        l_a = [1, 2, 3]
        cl_b = CustomList([3, 4])
        cl_c = l_a + cl_b
        self.assertListEqual(list(cl_c), [4, 6, 3])

        cl_a = CustomList([3])
        l_b = [1, 2]
        cl_c = cl_a + l_b
        self.assertListEqual(list(cl_c), [4, 2])

        l_a = [1, 2]
        cl_b = CustomList([3, 4, 10])
        cl_c = l_a - cl_b
        self.assertListEqual(list(cl_c), [-2, -2, -10])

        cl_a = CustomList([3, 4])
        l_b = [1]
        cl_c = cl_a - l_b
        self.assertListEqual(list(cl_c), [2, 4])

        cl_a = CustomList([3, 4])
        l_b = []
        cl_c = cl_a + l_b
        self.assertListEqual(list(cl_c), [3, 4])

        l_a = []
        cl_b = CustomList([3, 4])
        cl_c = l_a - cl_b
        self.assertListEqual(list(cl_c), [-3, -4])

    def test_types(self):
        self.assertIsInstance(
            CustomList([5, 1, 3, 7]) + CustomList([1, 2, 7]), CustomList
        )
        self.assertIsInstance(
            CustomList([5, 1, 3, 7]) - CustomList([1, 2, 7]), CustomList
        )

    def test_comparisons(self):
        self.assertTrue(CustomList([5, 7]) > CustomList([1, 2, 7]))
        self.assertTrue(CustomList([5, 7]) == CustomList([7, 5]))
        self.assertTrue(CustomList([8, 8]) != CustomList([7, 5]))
        self.assertTrue(CustomList([]) < CustomList([7]))
        self.assertTrue(CustomList([1, 1, 1, 1, 1]) == CustomList([5]))
        self.assertTrue(CustomList([5, 7]) <= CustomList([8, 5]))
        self.assertTrue(CustomList([5, 7]) >= CustomList([12]))

    def test_invariability(self):
        cl_a = CustomList([5, 1, 3, 7])
        cl_b = CustomList([1, 2, 7])
        cl_c = cl_a + cl_b
        self.assertListEqual(list(cl_a), [5, 1, 3, 7])
        self.assertListEqual(list(cl_b), [1, 2, 7])
        self.assertListEqual(list(cl_c), [6, 3, 10, 7])

        cl_a = CustomList([5, 1, 3, 7])
        cl_b = CustomList([1, 2, 7])
        cl_c = cl_a - cl_b
        self.assertListEqual(list(cl_a), [5, 1, 3, 7])
        self.assertListEqual(list(cl_b), [1, 2, 7])
        self.assertListEqual(list(cl_c), [4, -1, -4, 7])

    def test_str(self):
        self.assertEqual(str(CustomList([5, 1, 3, 7])), "[5, 1, 3, 7], 16")
        self.assertEqual(str(CustomList()), "[], 0")

    if __name__ == '__main__':
        unittest.main()
