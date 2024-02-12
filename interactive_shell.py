from e2_functions import *
import time
from matplotlib import pyplot as plt
import os
print('initiating interactive shell for data collection')
print('testing connections')
arduino_connect_and_send(instruction_generator(10000, [2000,200]))
with Picoscope(time_per_sample=f'80ns', probe_10x=True, trigger_channel='a') as scope:
    times, voltages_template, _ = scope.wait_for_key('s')
    print(times)
print("waiting for arduino")

shell_active = True
while shell_active == True:
# define range 
    sample_ns_user = int(input('input a desired picoscope sample time(ns): \n'))
# ask for arduino mode 
    arduino_mode = input('input arduino control mode(manual, auto(for half duty cycle only)):\n')
    runmode = 0
    delay_1 = 0
    delay_2 = 0
    delay_3 = 0
    delay_4 = 0
    message_str = ''
    #simply input the serial string to pass to arduino 
    if arduino_mode == 'manual':
        message_str = input('input the instruction string:\n')
    elif arduino_mode == 'auto':
        half_phase_period = int(input('input half phase period(micro_s): \n'))
        phase_delay_time = int(input('input phase delay:\n'))
        # allow arduino to run for 5000 ms, current hard coded setting, may change later
        message_str = instruction_generator(5000, [half_phase_period,phase_delay_time])
    else:
        pass
    arduino_connect_and_send(message_str)

    # process input sample time for picoscope 
    sample_instruction=closest_pico_time_per_sample(sample_ns_user)
    times_array = np.zeros(8064)
    voltages_array_a = np.zeros(8064)
    voltages_array_b = np.zeros(8064)
    times_array, voltages_array_a, voltages_array_b = use_pico_and_record(sample_instruction)
    # dislay viewing window 
    plt.plot(times_array,voltages_array_a)
    plt.plot(times_array,voltages_array_b)
    plt.show()

    # ask if save 
    if_save = input('save the file?(y/n)')
# ask for file name 
    if if_save == 'y':
        file_name = input('please input filename: \n')
        with open(f'{file_name}_instructions.txt', "w") as f:
            f.write(message_str)
        np.save(f'{file_name}_times.npy', times_array)
        np.save(f'{file_name}_voltages_a.npy', voltages_array_a)
        np.save(f'{file_name}_voltages_b.npy', voltages_array_b)
        print("file saved")
