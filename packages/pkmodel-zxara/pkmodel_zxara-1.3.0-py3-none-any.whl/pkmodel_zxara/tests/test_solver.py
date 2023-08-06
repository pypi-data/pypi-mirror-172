"""
    Unit tests for the functions in the PK_model_setup module
"""
import numpy as np
import unittest
#import pkmodel_zxara as pk
import pkmodel_zxara.solver as pkmod
from pkmodel_zxara.model import Model 

class rhs_Test(unittest.TestCase):
    """
    Tests the :function:`rhs`.
    """
    def test_create(self):
        """
        Tests rhs functions as expected for test case.
        """
        t = np.arange(0,10,0.1)
        y = np.array([1,1,0])
        central = [2,2] 
        periphal = [[1,2], [3,4], [4,5], [5,7]]
        ka = [3]
        dose_concentration = 4
        DOSAGE_COMPARTMENT = True
        test_rhs = pkmod.rhs(t, y, central, periphal, ka, dose_concentration, DOSAGE_COMPARTMENT)
        self.assertEqual(test_rhs.tolist(), [1, -7, 1, 2, 2.5, 3.5])
        
class Integrate_Test(unittest.TestCase):
    """
    Tests the :function: `Integrate` produces expected results.
    """
    def test_create(self):
        """
        Tests Protocol creation.
        """
        t_interval = np.arange(0,7.7,0.1)
        central = [2,1] 
        periphal = [[1,4], [0.5 ,4]]
        ka = [3]
        dose_concentration = 4
        DOSAGE_COMPARTMENT = False
        y0 = [0.1,0,4,3]
        test_t, test_y = pkmod.Integrate(t_interval, y0, central, periphal, ka, dose_concentration, DOSAGE_COMPARTMENT)
        self.assertEqual(test_t.tolist(), t_interval.tolist())
        self.assertEqual(test_y.shape[1], 77)
        self.assertAlmostEqual(np.mean(test_y), 2.81614284) 

class PK_solver_Test(unittest.TestCase):
    """
    Tests the :function:`PK_solver`.
    """
    def test_create(self):
        """
        Tests Protocol creation.
        """
        central = [2,1] 
        peripheral = [[1,4], [0.5 ,4]]
        ka = [3]
        TMAX = 10
        DOSE_REGIME = [[1,2.3,4], [3,3,1.3],[6.5,7,5]]
        
        sys_model = Model(central, peripheral, ka)
        
        ttest, ytest = pkmod.PK_solver(sys_model, TMAX, DOSE_REGIME)
        self.assertEqual(ytest.shape[0], 1001)
        self.assertAlmostEqual(np.mean(ytest), 0.7298813)

