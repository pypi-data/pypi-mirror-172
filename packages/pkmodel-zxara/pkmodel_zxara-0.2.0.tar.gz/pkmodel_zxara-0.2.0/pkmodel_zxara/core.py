from input import *
from model import Model
from protocol import Protocol

# Collect model input data 
central = central_input()
peripherals = peripheral_input()
dosage = dosage_input()

sys_model = Model(central, peripherals, dosage) # Create Model object

# Collect protocol input data
dosing_array = protocol_input_steady()
dosing_array = protocol_input_instantaneous(dosing_array)
MAX_TIME = max_time_input()

sys_protocol = Protocol(dosing_array, MAX_TIME)

# Add solver here

# Add plotting here

# Add return graphs and CSV here (CSV currently only outputs model input parameters)

save_csv(sys_model,dosing_array,MAX_TIME,filename = 'prototypemodel')


