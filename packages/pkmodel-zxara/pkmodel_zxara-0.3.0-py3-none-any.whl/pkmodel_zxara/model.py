#
# Model class
#

# function to catch type error in list
def catchTypeError(input_list):
    if len(input_list) != 2:
        raise ValueError('wrong number of inputs provided')
    for val in input_list:
        if int(val) < 0 or not isinstance(val, (float, int)):
            raise ValueError('input values should be non-negative numbers')


class Model:
    """
    Parameters
    ----------
    central: list, [central_volume, clearance_rate]
    peripherals: array of lists, [[compartment1_volume, transition_rate1], ...]
    dosage: list, 
          if i.b. dosing : empty list 
          if s.c dosing : list contains absorption rate KA
    
    Functions
    ----------
    pcount: int, number of peripheral compartments

    Exceptions
    -----------
    raise value error if a non numerical value or negative number is given as an input
    raise value error if k_a input is not an empty list, or list containing non negative number

    """
    def __init__(self, central, peripherals=[], dosage=[]):
        catchTypeError(central)
        for periph in peripherals:
            catchTypeError(periph)
        if len(dosage) not in [0,1] or (len(dosage) == 1 and not isinstance(dosage[0], (int, float))):
            raise ValueError('invalid k_a input')
        
        self.central = central
        self.peripherals = peripherals
        self.dosage = dosage

    @property
    def pcount(self):
        return len(self.peripherals)


