import numpy as np
from matplotlib import pyplot as plt

with open("datafile.csv") as datafile:
    data = np.loadtxt(datafile, delimiter=",", skiprows=1)

# Add converted (to GeV) electron energy values to array
ele_energy_array = []

for line in data:
    ele_energy_array.append(line[1]*1e-3) 

# Calculate the mean
mean = np.round(np.mean(ele_energy_array), 2)

# Plot the histogram
plt.hist(ele_energy_array, bins=50, range=(-50, 400))
plt.ylabel('Number of events')
plt.xlabel('Electron energy [GeV]')
plt.text(200, 550, r'$\overline{E}=$' + str(mean) + 'GeV')
plt.grid(True)
plt.savefig('electron_energy_p.png')
plt.show()
