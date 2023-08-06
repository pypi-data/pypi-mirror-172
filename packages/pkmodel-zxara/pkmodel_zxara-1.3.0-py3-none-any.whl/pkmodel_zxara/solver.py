#%%
'''
INPUTS
    Number of peripheral compartments (n int)
    Dose regime (constant or times, amount pairs)
    Dose compartment (True/False)
    Protocols (transitions Q, volumes V and clearance CL)
'''
import matplotlib.pyplot as plt
import numpy as np
import scipy.integrate

#############
# Function generating rhs of ODEs
#############

def rhs(t, y, central, periphal, ka, dose_concentration, DOSAGE_COMPARTMENT):
    '''
    t       : time, independant
    y       : [q_dosage, q_central, q_periphal_1, ..., q_periphal_n]
    central : [VC, CL]
    periph  : [ [Q1,V1],..., [Qn,Vn] ]
    ka      : subcutaneous dosing absorption rate, possibly None
    '''
    qd = np.array([y[0]])
    qc = np.array([y[1]])
    qp = np.array(y[2:]) #What happens if empty?
    VC, CL = central
    Qp = np.array([item[1] for item in periphal])
    Vp = np.array([item[0] for item in periphal])

    if DOSAGE_COMPARTMENT:
        Dqd = dose_concentration - ka*qd
        Dqc =   ka*qd   - CL*qc/VC - sum( Qp*(qc/VC - qp/Vp) )
    else:
        Dqd = np.array([0])
        Dqc = dose_concentration - CL*qc/VC - sum( Qp*(qc/VC - qp/Vp) )

    Dqp = Qp*(qc/VC - qp/Vp)

    return np.concatenate((Dqd,Dqc,Dqp))

#############
# ODE Integration
#############

def Integrate(t_interval, y0, central, periphal, ka, dose_concentration, DOSAGE_COMPARTMENT):
    args = (central, periphal, ka, dose_concentration, DOSAGE_COMPARTMENT)
    sol = scipy.integrate.solve_ivp(
            fun=lambda t, y: rhs(t, y, *args),
            t_span=[t_interval[0], t_interval[-1]],
            y0=y0, 
            t_eval=t_interval)
    
    return sol.t, sol.y

#############
# ODE Solver
#############

def PK_solver(sys_model, TMAX, DOSE_REGIME):
    
    """Function that solves the ODEs for a given system and dosage regime
    
    Parameters:
        sys_model: Model object of the system with user specified features
        TMAX: The maximum time of the interval
        DOSE_REGIME: A list of dose specifications for each dose. 
                    Each dose specification takes the form of the following list: [start time, end time, total dose]
    Returns:
        tsol: array of time points corresponding to elements in ysol
        ysol: array of concentrations of the drug in each compartment. 
              Rows represent compartments 
              Columns represent time points.
    """

    central = sys_model.central
    peripheral = sys_model.peripherals
    ka = sys_model.dosage
    NUM_OF_PCS = sys_model.pcount

    DOSAGE_COMPARTMENT = False
    if len(ka) == 1:
        DOSAGE_COMPARTMENT = True
    
    # initialise variables
    t0 = 0
    dose_concentration = 0
    y0 = np.zeros(2 + NUM_OF_PCS)
    # initialise time and concentration data structures
    tsol = []
    ysol = np.zeros((2 + NUM_OF_PCS,1))

    for dosage in DOSE_REGIME:
        ## PRE-DOSE INTERVAL
        t_interval = np.arange(t0,dosage[0],TMAX/1000) # Increment dosage concentration at start of t_interval
        sol_t, sol_y = Integrate(t_interval, y0, central, peripheral, ka, dose_concentration, DOSAGE_COMPARTMENT)
        tsol.append(sol_t)
        ysol = np.hstack([ysol,sol_y])
        # update initial compartmental concentration values for next interval
        y0 = sol_y[:,-1]
        dose_concentration = 0


        ## DOSE INTERVAL
        
        ## for an instantaneous dose
        if dosage[0]==dosage[1]:
            if DOSAGE_COMPARTMENT: 
                y0[0] += dosage[2] # if subcutaneous dose adds to dose compartment
            else:
                y0[1] += dosage[2] # if intravenous dose adds directly to central
            t0 = dosage[0]
       
        ## for the continuous treatment
        else:
            t_interval = np.arange(dosage[0],dosage[1],TMAX/1000)
            dose_concentration = dosage[2]/(dosage[1]-dosage[0]) # change total dose to dose rate
            sol_t, sol_y = Integrate(t_interval,y0, central, peripheral, ka, dose_concentration, DOSAGE_COMPARTMENT)
            tsol.append(sol_t)
            ysol = np.hstack([ysol,sol_y])
            y0 = sol_y[:,-1]
        
        t0 = dosage[1]
        dose_concentration = 0

    # interval after final dose
    t_interval = np.arange(t0,TMAX,TMAX/1000)
    sol_t, sol_y = Integrate(t_interval,y0, central, peripheral, ka, dose_concentration, DOSAGE_COMPARTMENT)
    tsol.append(sol_t)
    ysol = np.hstack([ysol, sol_y])
    
    # reshape data 
    tsol = np.concatenate((tsol))
    tsol = np.transpose(np.tile(tsol, (len(ysol),1)))
    ysol = np.transpose(ysol[:,1:])

    return tsol, ysol
# %%


