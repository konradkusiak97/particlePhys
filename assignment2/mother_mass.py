import numpy as np
from matplotlib import pyplot as plt
import random

W_MASS = 80.377 # +/- 0.012 GeV
T_MASS_MAX = 250.0 # GeV

def pick_W_jets(jet1_4EM, jet2_4EM, jet3_4EM):
    result_12 = 0
    result_23 = 0
    result_31 = 0
    for count, (j1, j2, j3) in enumerate(zip(jet1_4EM, jet2_4EM, jet3_4EM)):
        if count == 0:
            result_12 += np.power(j1+j2,2)
            result_23 += np.power(j2+j3,2)
            result_31 += np.power(j3+j1,2)
        else:
            result_12 -= np.power(j1+j2,2)
            result_23 -= np.power(j2+j3,2)
            result_31 -= np.power(j3+j1,2)
    
    result_12 = np.sqrt(result_12)
    result_23 = np.sqrt(result_23)
    result_31 = np.sqrt(result_31)

    results_arr = np.array([result_12, result_23, result_31])
    closest_idx = np.argmin(np.fabs(results_arr - W_MASS))

    return closest_idx

def calc_top_mass(b1_jet, b2_jet, jet1, jet2):
    result1 = 0
    result2 = 0
    for count, (b1, b2, j1, j2) in enumerate(zip(b1_jet, b2_jet, jet1, jet2)):
        if count == 0:
            result1 += np.power(b1+j1+j2,2)
            result2 += np.power(b2+j1+j2,2)
        else:
            result1 -= np.power(b1+j1+j2,2)
            result2 -= np.power(b2+j1+j2,2)

    result1 = np.sqrt(result1)
    result2 = np.sqrt(result2)

    if result1 < T_MASS_MAX and result2 < T_MASS_MAX:
        return random.choice([result1, result2]) 
    elif result1 < T_MASS_MAX:
        return result1
    elif result2 < T_MASS_MAX:
        return result2
    else:
        # not record the result in this case
        return 0
            
    
with open("datafile.csv") as datafile:
    data = np.loadtxt(datafile, delimiter=",", skiprows=1)

# Store the final results in the array
t_mass_results = []

# Calculate the rest mass for each event and append the result to the array
for line in data:
    b1_jet4EM = np.array([line[5], line[6], line[7], line[8]])*1e-3
    b2_jet4EM = np.array([line[9], line[10], line[11], line[12]])*1e-3
    jet1_4EM = np.array([line[13], line[14], line[15], line[16]])*1e-3
    jet2_4EM = np.array([line[17], line[18], line[19], line[20]])*1e-3
    jet3_4EM = np.array([line[21], line[22], line[23], line[24]])*1e-3

    idx = pick_W_jets(jet1_4EM, jet2_4EM, jet3_4EM)
    if idx == 0 : 
        t_mass = calc_top_mass(b1_jet4EM, b2_jet4EM, jet1_4EM, jet2_4EM)
        if t_mass != 0:
            t_mass_results.append(t_mass)
    elif idx == 1 :
        t_mass = calc_top_mass(b1_jet4EM, b2_jet4EM, jet2_4EM, jet3_4EM)
        if t_mass != 0:
            t_mass_results.append(t_mass)
    else:
        t_mass = calc_top_mass(b1_jet4EM, b2_jet4EM, jet1_4EM, jet3_4EM)
        if t_mass != 0:
            t_mass_results.append(t_mass)

# Calculate the mean
mean = np.round(np.mean(t_mass_results), 2)

# Find standard deviation
std = np.round(np.std(t_mass_results))

# Plot the histogram
plt.hist(t_mass_results, bins=80)
plt.ylabel('Number of events')
plt.xlabel('anti(top) mass [GeV]')
plt.text(85, 10, r'$\overline{m}=$' + str(mean) + r'$\pm$' + str(std) + 'GeV')
plt.grid(True)
plt.savefig('t_mass_plot_hist.png')
plt.show()
