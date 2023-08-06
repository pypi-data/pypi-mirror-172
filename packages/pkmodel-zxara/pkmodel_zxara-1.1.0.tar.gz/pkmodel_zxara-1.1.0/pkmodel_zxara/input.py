from locale import strcoll

def check_error(variable, type_var, input_string):
    '''
    Function to continue asking for input until it is the right type`;
        variable: variable to be inputted
        type_var: requested type of variable
        input_string: user prompt
    
    Returns:
        variable: variable in correct type

    '''
    while True:
        try:
            variable = type_var(input(input_string))
        except ValueError:
            print("Incorrect type try again")
            continue
        else:
            return variable


def check_error_string_input(variable, accepted_input, input_string):
    '''
    Function to continue asking for input until it is the right letter
        variable: variable to be inputted
        accepted_input: desired input (eg 'Y' or 'N')
        input_string: user prompt
    
    Returns:
        variable: variable in upper case of desired letter
    '''

    while True:
        try:
            variable = input(input_string)
            if variable.upper() != accepted_input[0] and variable.upper() != accepted_input[1]:
                raise ValueError
        except ValueError:
            print("Incorrect type try again")
            continue
        else:
            return variable.upper()

       
def central_input():
    """
    Collect central compartment data from user input:
        Volume, VC / mL
        Clearance rate, CL / mL/h

    Returns:
    central (list): central compartment parameters [VC, CL]
    """
    VC = None
    VC = check_error(VC, float, 'Volume of central compartment in mL: ')
    
    CL = None
    CL = check_error(CL, float, 'Clearance rate from central compartment in mL/h: ')

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
    NUM_OF_PCS = None
    NUM_OF_PCS = check_error(NUM_OF_PCS, int, 'Number of peripheral compartments: ')

    peripherals = []
    for i in range(0,NUM_OF_PCS):
        VP = None
        VP = check_error(VP,float,(f'Volume of peripheral compartment {i+1} in mL: '))

        QP = None
        QP = check_error(QP, float,(f'Transition rate between central compartment and peripheral compartment {i+1} in mL/h: '))
        
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
    DOSAGE_COMPARTMENT = None
    DOSAGE_COMPARTMENT = check_error_string_input(DOSAGE_COMPARTMENT, ['Y','N'],'Is there a dosage compartment (Y/N)? ')

    dosage = []
    if DOSAGE_COMPARTMENT == 'Y':
        k_a = None
        k_a = check_error(k_a, float, 'Absorption rate for dosage compartment (/h) if subcutaneous dosing: ')
        dosage.append(k_a)
    
    return dosage

def input_doses():
    '''
    Collect number of doses, whether they are steady or instantaneous, and what amount of drug is given
    '''
    TOTAL_DOSES = None
    TOTAL_DOSES = check_error(TOTAL_DOSES,int,'How many total doses is the individual given (steady or continuous)? ')
    dosing_array = []

    previous_end_time = 0

    for i in range(1,TOTAL_DOSES+1):
        print('Dose ' + str(i) + ':')
        DOSE_TYPE = None
        DOSE_TYPE = check_error_string_input(DOSE_TYPE,['A','B'],'Is drug given in steady application over time (A) or instantaneously (B)? ')

        if DOSE_TYPE == 'A':
            DOSE_RATE = None
            DOSE_RATE = check_error(DOSE_RATE,float,'Dosage rate of drug given (ng/h): ')

            START_TIME = None
            START_TIME = check_error(START_TIME,float,'Start time (h): ')

            while START_TIME <= previous_end_time:
                print('Input of dose has to begin after end of preceding dose')
                START_TIME = check_error(START_TIME,float,'Start time (h): ')

            END_TIME = None
            END_TIME = check_error(END_TIME,float,'End time (h): ')

            previous_end_time = END_TIME
            
            DOSE = DOSE_RATE * (END_TIME - START_TIME)
        
            # Make dosing array
            dosing_array.append([START_TIME, END_TIME, DOSE])
        
        if DOSE_TYPE == 'B':
            DOSE = None
            DOSE = check_error(DOSE, float, 'Instantaneous dose of drug given per time point (ng): ')

            TIME_POINT = None
            TIME_POINT = check_error(DOSE,float,'Time point at which drug is given (h): ')

            if TIME_POINT <= previous_end_time:
                print('Input of dose has to begin after end of preceding dose')
                TIME_POINT = check_error(TIME_POINT,float,'Time point at which drug is given (h): ')

            previous_end_time = TIME_POINT

            dosing_array.append([TIME_POINT, TIME_POINT, DOSE])

    return dosing_array

def max_time_input():
    """
    Collect maximum time user input
    
    Returns:
    MAX_TIME (float): maximum time for modelling / h
    """
    MAX_TIME = None
    MAX_TIME = check_error(MAX_TIME,float,'Enter maximum time for model (h): ')
    return MAX_TIME