import numpy as np
from matplotlib import pyplot as plt

# Function that calculates the rest mass of the mother particle in the units of GeV
# Assumes the 4-vectors for ele and pos have values in GeV
def calc_mass(ele_4P, pos_4P):
    result = 0
    for count, (e, p) in enumerate(zip(ele_4P, pos_4P)):
        if count == 0:
            result += np.power(e+p,2)
        else:
            result -= np.power(e+p, 2) 
    return np.sqrt(result)
    
with open("datafile.csv") as datafile:
    data = np.loadtxt(datafile, delimiter=",", skiprows=1)

# Store the final results in the array
mass_results = []

# Calculate the rest mass for each event and append the result to the array
for line in data:
    ele_4P = np.array([line[1], line[2], line[3], line[4]])
    pos_4P = np.array([line[5], line[6], line[7], line[8]])
    mass_results.append(calc_mass(ele_4P*1e-3, pos_4P*1e-3))

# Calculate the mean
mean = np.round(np.mean(mass_results), 2)

# Plot the histogram
plt.hist(mass_results, bins=50, range=(60, 120))
plt.ylabel('Number of events')
plt.xlabel('Mother particle rest mass [GeV]')
plt.text(70, 500, r'$\overline{m}=$' + str(mean) + 'GeV')
plt.grid(True)
plt.savefig('mother_mass_plot.png')
plt.show()
