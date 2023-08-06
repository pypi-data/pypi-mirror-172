def central_input():
    """
    Collect central compartment data from user input:
        Volume, VC / mL
        Clearance rate, CL / mL/h

    Returns:
    central (list): central compartment parameters [VC, CL]
    """
    # TODO: Fail if input anything except int or float
    VC = float(input('Volume of central compartment in mL: '))
    CL = float(input('Clearance rate from central compartment in mL/h: '))
    central = [VC, CL]
    
    return central


def peripheral_input():
    """
    Collect peripheral compartment(s) data from user input:
        Number of compartments
        Volume, V / mL of each compartment
        Transition rate, Q / mL/h of each compartment

    Returns:
    peripherals (list of lists): peripheral compartment parameters [[V1, Q1], [V2, Q2]]
        - empty list if no peripheral compartments
    """
    # TODO: Fail if input anything except int
    NUM_OF_PCS = int(input('Number of peripheral compartments (0, 1, or 2): '))

    peripherals = []
    for i in range(0,NUM_OF_PCS):
         # TODO: Fail if input anything except int or float
        VP = float(input(f'Volume of peripheral compartment {i+1} in mL: '))
        QP = float(input(f'Transition rate between central compartment and peripheral compartment {i+1} in mL/h: '))
        peripherals.append([VP,QP])
    
    return peripherals



def dosage_input():
    """
    Determine dosage compartment existence and parameters from user input:
        Absorption rate k_a / /h

    Returns:
    dosing (list): dosage compartment parameters [k_a]
        - empty list if no dosage compartment
    """
    DOSAGE_COMPARTMENT = input('Is there a dosage compartment (Y/N)? ')

    dosage = []
    if DOSAGE_COMPARTMENT == 'Y':
        k_a = float(input('Absorption rate for dosage compartment (/h) if subcutaneous dosing: '))
        dosage.append(k_a)
    
    return dosage


def protocol_input_steady():
    """ 
    Collect steady dosage protocol from user input
    Returns:
    """
    # TODO: Fail if input anything except Y/N
    STEADY_DOSAGE = input('Is drug given in steady application over time (Y/N)? ')
    # Make dosing_array
    dosing_array = []

    if STEADY_DOSAGE == 'Y':
        DOSE_RATE = float(input('Dosage rate of drug given (ng/h): ')) # TODO: Only int or float
        print('Input time period during which drug is given:')
        START_TIME = float(input('Start time (h): ')) # TODO: Only int or float
        END_TIME = float(input('End time (h): ')) # TODO: Only int or float
        DOSE = DOSE_RATE * (END_TIME - START_TIME)
        
        # Make dosing array
        dosing_array = [[START_TIME, END_TIME, DOSE]]
        return dosing_array
    
    else:
        dosing_array = []
        return dosing_array

def protocol_input_instantaneous(dosing_array):
    """ 
    Collect instantaneous dosage protocol from user input and adds to array created for steady dosage (empty if only instanteous dosage)
    Returns:
    """
    INSTANTANEOUS_DOSAGE = input('Is drug given at instantaneous time points (Y/N)? ')

    if INSTANTANEOUS_DOSAGE == 'Y': 
        DOSE = int(input('Instantaneous dose of drug given per time point (ng): ')) # TODO: Only int or float
        
        # Create time points list
        TIME_POINTS = [] 
        add_point = 'Y'
        while add_point != 'N':
                TIME_POINTS.append(float(input('Time point at which drug is given (h): ')))
                add_point = input('Add another point (Y/N)? ')
        TIME_POINTS.sort()
                
        for t in TIME_POINTS:
            dosing_array.append([t, t, DOSE])
        
        # sort full dosing array by the first time point of both instantaneous and steady dosage 
        dosing_array.sort()
    
    return dosing_array

def max_time_input():
    """ # TODO: docstring """
    MAX_TIME = input('Enter maximum time for model (h): ')
    return MAX_TIME