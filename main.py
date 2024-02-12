from PLL_Lib import Picoscope
import serial
import serial.tools.list_ports
import time
import numpy as np
from matplotlib import pyplot as plt
from e2_functions import *
# main loop
#
#
#Generate tasks 
#tasks_todo = task_populator_linear(5,2000,100,-1,1,7)
#Pico_sample_time = 10
#with Picoscope(time_per_sample=f'20ns', probe_10x=True, trigger_channel='a') as scope:
#
#    times, voltages_template, _ = scope.wait_for_key('s')
#    print(times)

tasks_todo_raw = []

prob_array = np.flip(np.arange(0,1.05,0.05))
gap_array = list(range(0,10))
pulse_array = list(range(0, 10))
hp_array = list(range(20,25))


tasks_todo_raw = noise_array_generator_regular_pulse_batch(pulse_array, hp_array)
tasks_todo_raw = noise_command_existance_batch(prob_array, hp_array)
tasks_todo_raw = noise_command_simple_gap_batch(gap_array, hp_array)



prob_array_np = np.array(prob_array)
tasks_todo_np_raw = np.array(tasks_todo_raw)
# tasks_todo_np_raw = np.load('./simple_gap_800waves_320ns/command_in.npy')
print(tasks_todo_np_raw)
Pico_sample_time = 1800
times_array, voltages_array_a, voltages_array_b = tasks_execute_raw_command_manual_sample_time(tasks_todo_np_raw, Pico_sample_time)
print(times_array)
print(voltages_array_a)
print(voltages_array_b)
#np.save("prob_details.npy",prob_array_np)
np.save('command_in.npy',tasks_todo_np_raw)
np.save('times.npy',times_array)
np.save('voltages_a.npy',voltages_array_a)
np.save('voltages_b_input.npy',voltages_array_b)
plt.plot(times_array[0], voltages_array_a[0])
plt.show()
