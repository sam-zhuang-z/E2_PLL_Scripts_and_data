from matplotlib import pyplot as plt
cap = [1, 3.3, 10, 33, 100, 330]
period = [0.00007492, 0.0002504, 0.00070528, 0.00246016, 0.00700416, 0.06918144]

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
plt.plot(cap,period, marker = '+')
ax.set_title("Oscillation Period of VCO with Different Capacitance")
ax.set_xscale('log')
ax.set_xlabel('Capacitance/nf')
ax.set_yscale('log')
ax.set_ylabel('Period/s')
plt.show()
