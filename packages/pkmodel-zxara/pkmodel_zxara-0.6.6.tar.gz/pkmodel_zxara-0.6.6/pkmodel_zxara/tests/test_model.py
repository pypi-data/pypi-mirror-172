import unittest
import pkmodel_zxara as pk
class ModelTest(unittest.TestCase):
    """
    Tests the :class:`Model` class.
    """
    def test_create(self):
        """
        Tests Model creation.
        """
        model = pk.model.Model([5.5, 0], [[1,2],[0.001, 2], [5,6]], [5.5])
        self.assertEqual(model.central, [5.5, 0])
        self.assertEqual(model.peripherals, [[1,2],[0.001, 2], [5,6]])
        self.assertEqual(model.dosage, [5.5])

    def test_pcount(self):
        """
        Tests Model counts peripheral compartments.
        """
        model = pk.model.Model([5.5, 6.1], [[1,2],[0.001, 2]], [])
        self.assertEqual(model.pcount, 2)

        # case where no peripheral compartments
        model = pk.model.Model([5.5, 6.1], [], [8])
        self.assertEqual(model.pcount, 0)

    
    def test_valueTypes(self):
        """
        Tests Model rejects negative numbers and strings.
        """
        with self.assertRaises(ValueError):
            model = pk.model.Model([5.5, -0.3], [[1,2],[0.001, 2], [1,5]], [])
        with self.assertRaises(TypeError):
            model = pk.model.Model([5.5, 0.3], [[1000,2],[12, 'k']], [])
        # no peripheral compartment
        with self.assertRaises(ValueError):
            model = pk.model.Model([5.5, 0.3], [[1,2]], ['99'])

    
    def test_inputForm(self):
        """
        Tests Model rejects invalid input forms.
        """
        with self.assertRaises(ValueError):
            model = pk.model.Model([5.5, 0.3, 8], [[1,2],[0.001, 2]], [])
        with self.assertRaises(ValueError):
            model = pk.model.Model([5.5, 0.3], [[1,2],[0.001, 2,9],], [])
        with self.assertRaises(ValueError):
            model = pk.model.Model([5.5, 0.3], [[1,2],[0.001, 2,9],], [1, 2])
    
    
    
        



