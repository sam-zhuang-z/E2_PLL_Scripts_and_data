import numpy as np 
from matplotlib import pyplot as plt 

instructions = np.load('./exp_details.npy')
times = np.load("./times.npy")
vol_a = np.load('./voltages_a.npy')
vol_b = np.load('./voltages_b.npy')

N = 80
print(instructions[N])
plt.plot(times[N],vol_a[N])
plt.plot(times[N],vol_b[N])
plt.show()
