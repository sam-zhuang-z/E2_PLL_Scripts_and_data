from matplotlib import pyplot as plt 
import numpy as np 
from os import listdir 
from os import makedirs


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


target_dir = "./"

files = listdir(target_dir)
voltages_files = [file for file in files if file.endswith("voltages_a.npy")]
time_files = [file for file in files if file.endswith("times.npy")]

#asking each axis
timefile = ""
for file_name in time_files:
    plot_this = input(f"is this time file(y/n): {file_name}")
    if plot_this == "y":
        timefile = file_name
#loading time file 
time_axis_single = np.load(target_dir+timefile)

axisfile = ""
for file_name in voltages_files:
    plot_this = input(f"is this volt file(y/n): {file_name}")
    if plot_this == "y":
        axisfile = file_name
#loading time file 
voltages_single = np.load(target_dir+axisfile)

voltage_triggers = sweeping_trigger_marker(voltages_single)
print(voltage_triggers)

clock_closest_element = min(voltage_triggers, key=lambda x: abs(time_axis_single[x[0]]))
clock_zero_index = voltage_triggers.index(clock_closest_element)

print(period_duty_determination(time_axis_single,voltage_triggers,clock_zero_index))

""""
timefile = ""
for file_name in time_files:
    plot_this = input(f"is this time file(y/n): {file_name}")
    if plot_this == "y":
        timefile = file_name
#loading time file 
time_axis_single = np.load(target_dir+timefile)

#asking for axis files and plot at the same time
nextfile = True
while nextfile:
    for file_name in npy_files:
        plot_this = input(f"include this(y/n): {file_name}")
        if plot_this == "y":
            axis_holder = np.load(target_dir+file_name)
            plt.plot(time_axis_single, axis_holder, label = input("input label name: \n"))
    if_continue = input("continue(y/n)")
    if if_continue != "y":
        nextfile = False
plt.legend(loc='upper right', fontsize = 10)
plt.show()

"""


