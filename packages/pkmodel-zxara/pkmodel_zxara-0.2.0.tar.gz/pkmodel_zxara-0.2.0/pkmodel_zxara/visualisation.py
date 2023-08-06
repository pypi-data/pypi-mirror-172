# function that plots different pharmacokinetic models as different subplots
import numpy as np

def plotPK(time, concentration, n_models):    
    '''Plot pharmacokinetic models.

    Plots different pharmacokinetic models next to each other.
 
    :param time: list of time points
    :param concentration: list of concentration points
    :param n_models: integer defining number of pharmacokinetic models to plot
    :returns: None, saves plot under PKplot.png
    '''

    import matplotlib.pyplot as plt
  
    fig, axes = plt.subplots(nrows= 1, ncols= n_models)

    if n_models == 1: #otherwise error that AxesSubplot object is not subscriptable

        axes.plot(time, concentration)
        axes.set_title('model 1')
        axes.set_ylabel('drug mass [ng]')
        axes.set_xlabel('time [h]')
        axes.legend(['q1', 'q2', 'q3', 'q4', 'q5'])
    
    else:

        for i in range(n_models):
            
            j = i+1 # axes and array indices start with zero while model should start with 1
            axes[i].plot(time[i], concentration[i])
            axes[i].set_title(f'model {j}')
            axes[i].set_ylabel('drug mass [ng]')
            axes[i].set_xlabel('time [h]')
            axes[i].legend(['q1', 'q2', 'q3', 'q4', 'q5'])
    
    
    fig.tight_layout()
    fig.savefig("PKplot.png")
    plt.show()

# plotPK(np.array([[1,2,3],[2,3,1],[3,1,2]]), np.array([[4,5,6],[5,6,4],[6,4,5]]), 3) this is how i thought the input would look like
