import unittest
import pkmodel_zxara as pk


class SolutionTest(unittest.TestCase):
    """
    Tests the :class:`Solution` class.
    """
    def test_create(self):
        """
        Tests Solution creation.
        """
        model = pk.Solution()
        self.assertEqual(model.value, 44)

