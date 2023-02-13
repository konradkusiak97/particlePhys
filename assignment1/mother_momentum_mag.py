import numpy as np
from matplotlib import pyplot as plt

# Function that calculates the magnitude of the momentum of mother particle
# Assumes momentum vectors have GeV units
def calc_momentum_mag(ele_P, pos_P):
    result = 0
    for (e, p) in zip(ele_P, pos_P):
        result += np.power(e+p,2)
    return np.sqrt(result)
    
with open("datafile.csv") as datafile:
    data = np.loadtxt(datafile, delimiter=",", skiprows=1)

# Store the final results in the array
momentum_mag_results = []

# Calculate the magnitude of momentum of mother particle for each event
for line in data:
    ele_P = np.array([line[2], line[3], line[4]])
    pos_P = np.array([line[6], line[7], line[8]])
    momentum_mag_results.append(calc_momentum_mag(ele_P*1e-3, pos_P*1e-3))

# Calculate the mean
mean = np.round(np.mean(momentum_mag_results), 2)

# Plot the histogram
plt.hist(momentum_mag_results, bins=50, range=(-100, 600))
plt.ylabel('Number of events')
plt.xlabel('Mother particle momentum magnitude [GeV]')
plt.text(300, 350, r'$\overline{p}=$' + str(mean) + 'GeV')
plt.grid(True)
plt.savefig('momentum_plot.png')
plt.show()
