from matplotlib import pyplot as plt
import numpy as np
from os import listdir 
from os import makedirs

target_dir = "./"

files = listdir(target_dir)


def sweeping_trigger_marker(input_array):
    trigger_markers = [] # [position,"up"]
    prev_value = input_array[0]
    for i in range(1, len(input_array)):
        if input_array[i-1] < 2.5 < input_array[i] :
            trigger_markers.append([i, 1])
        elif input_array[i] < 2.5 < input_array[i-1]:
            trigger_markers.append([i, -1])
        prev_value = input_array[i]
    return trigger_markers

## duty cycle determination function 
#### should input a index in trigger_marker 
#### batch processing will come later after determining time-zero point 
#### if input point is invalid, return negative number
def period_duty_determination(times_array, input_marker_array, up_index):
### verify the index indicate a rising edge 
    ##pos pos(+2) gives a full cycle period
    start_index = input_marker_array[up_index][0]
    turn_index = input_marker_array[up_index+1][0]
    end_index = input_marker_array[up_index+2][0]

    duty_cycle = (times_array[turn_index] - times_array[start_index])/(times_array[end_index] - times_array[start_index])
    period = times_array[end_index] - times_array[start_index]
    return period, duty_cycle

def zero_trigger_determination(marker_array, times_array):
    zero_index = -1
    closest_zero_element = min(marker_array, key=lambda x: abs(times_array[x[0]]))
    zero_index = marker_array.index(closest_zero_element)
    return zero_index


period_list = []
mean_voltage_array = []
for i in range(1,9):
    #constructing names for the selection 
    times_array = np.load(f"./vco_voltage_3300pf_100k_100k_{i}_times.npy")
    voltages_a = np.load(f"./vco_voltage_3300pf_100k_100k_{i}_voltages_a.npy")
    voltages_b = np.load(f"./vco_voltage_3300pf_100k_100k_{i}_voltages_b.npy")
    voltages_a_trigger = sweeping_trigger_marker(voltages_a)
    zero_index = zero_trigger_determination(voltages_a_trigger, times_array)
    period, duty_cycle = period_duty_determination(times_array, voltages_a_trigger, zero_index)
    mean_voltage = np.mean(voltages_b)
    period_list.append(period)
    mean_voltage_array.append(mean_voltage)


fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.plot(mean_voltage_array, period_list)
ax.set_ylabel("vco period/s")
ax.set_title("Relationship Between VCO Output Period and Control Voltage")
ax.set_xlabel("control voltage/V")
plt.show()






