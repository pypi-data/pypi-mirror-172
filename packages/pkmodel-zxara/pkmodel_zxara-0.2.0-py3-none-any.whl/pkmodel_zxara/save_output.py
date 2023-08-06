import csv

'''
Module to save model parameters as well as solution output
'''

def save_csv(model,dosing_array,max_time,filename):

    input_dict = vars(model)

    # rename keys to make more detailed
    input_dict['Central compartment (volume in mL, clearance in mL/h)'] = input_dict.pop('central')
    input_dict['Peripheral compartment(s) (volume in mL, transition rate in mL/h)'] = input_dict.pop('peripherals')
    input_dict['Absorption rate for dosage compartment (/h) if subcutaneous dosing'] = input_dict.pop('dosage')
    input_dict['Start/end time of dose and dose amount (ng)'] = dosing_array
    input_dict['Maximum time'] = max_time

    with open(filename+'.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=input_dict.keys())
        writer.writeheader()
        writer.writerow(input_dict)
    
    # TODO: add solution output and save as csv