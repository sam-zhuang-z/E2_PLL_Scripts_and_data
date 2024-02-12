from PLL_Lib import Picoscope
import serial
import serial.tools.list_ports
import time
import numpy as np
import random
from matplotlib import pyplot as plt

def arduino_connect_and_send(message):
    ports = list(serial.tools.list_ports.comports())
    ard_port = ''
    # find which port is on arduino
    for p in ports:
        if 'arduino' in p.description.lower():
            ard_port = p.device
            print(f'arduino found on port {ard_port}')
    
    # open serial port
    ard_ser = serial.Serial(ard_port, baudrate= 9600)
    #wait for the port to open properly
    time.sleep(2)
    
    send_bytes =  bytes(message, 'utf-8')
    ard_ser.write(send_bytes)

def arduino_connect_and_send_wait_on_return(message):
    ports = list(serial.tools.list_ports.comports())
    ard_port = ''
    # find which port is on arduino
    for p in ports:
        if 'arduino' in p.description.lower():
            ard_port = p.device
            print(f'arduino found on port {ard_port}')
    
    # open serial port
    ard_ser = serial.Serial(ard_port, baudrate= 9600)
    #wait for the port to open properly
    time.sleep(2)
    
    send_bytes =  bytes(message, 'utf-8')
    ard_ser.write(send_bytes)
    return ard_ser.readline()



# an iterator that returns a 2D array with raw tasks
# shoud return in form of ((half-period(microsecond),phase delay time(microsecond)),(),())
def task_populator_linear(start_hp,end_hp,hp_scan_density,start_phase_delay_ratio,end_phase_delay_ratio,num_of_phase_delay_sample):
    task_list = []
    hp_populator = start_hp
    task_single = []
    while hp_populator <= end_hp:
        start_phase_delay = hp_populator*start_phase_delay_ratio
        end_phase_delay = hp_populator*end_phase_delay_ratio
        phase_delay_list = np.linspace(start_phase_delay, end_phase_delay, num_of_phase_delay_sample).round().astype(int).tolist()
        for phase_delay_element in phase_delay_list:
            task_single = [hp_populator, phase_delay_element]
            task_list.append(task_single)
        hp_populator += hp_scan_density
    return task_list

def task_populator_exp(start_hp,end_hp,hp_count,start_phase_delay_ratio,end_phase_delay_ratio,num_of_phase_delay_sample):
    task_list = []
    hp_populator = start_hp
    task_single = []
    hp_list = np.geomspace(start_hp, end_hp, hp_count).round().astype(int).tolist()
    for hp_populator in hp_list:
        start_phase_delay = hp_populator*start_phase_delay_ratio
        end_phase_delay = hp_populator*end_phase_delay_ratio
        phase_delay_list = np.linspace(start_phase_delay, end_phase_delay, num_of_phase_delay_sample).round().astype(int).tolist()
        for phase_delay_element in phase_delay_list:
            task_single = [hp_populator, phase_delay_element]
            task_list.append(task_single)
    return task_list
# convert an element of task list and convert it to strings to be interpreted by arduino 

def instruction_generator(operation_time, task_list_single):
    runmode = -1
    offset_1 = 0
    offset_2 = 0
    offset_3 = 0
    offset_4 = 0
    #determine type of wave(which one is leading)
    if task_list_single[1] == 0:
        runmode = 0
        offset_1 = task_list_single[0]
        offset_2 = task_list_single[0]-1
    elif task_list_single[1] > 0:
        runmode = 1
        offset_1 = task_list_single[1]
        offset_2 = task_list_single[0]-task_list_single[1]
        offset_3 = task_list_single[1]
        offset_4 = max(0,task_list_single[0]-task_list_single[1] - 1)

    elif task_list_single[1] < 0:
        runmode = 2
        offset_1 = -task_list_single[1]
        offset_2 = task_list_single[0]+task_list_single[1]
        offset_3 = -task_list_single[1]
        offset_4 = max(0,task_list_single[0]+task_list_single[1] - 1)


    #string maniputation
    # consideration of cpu cycles for register change and adjust accordingly current method:
    # reduce one microsecond of delay on the last offset
    return f"({operation_time},{runmode},{offset_1},{offset_2},{offset_3},{offset_4})"

def convert_sequences_command(noise_array):
    result = ""
    current_sequence = 0
    current_value = noise_array[0]

    for value in noise_array:
        if value == current_value:
            current_sequence += 1
        else:
            result += str(current_sequence) if current_value else str(-current_sequence)
            result += ","
            current_sequence = 1
            current_value = value

    result += str(current_sequence) if current_value else str(-current_sequence)
    return result


def noise_array_generator_single_existance(prob_of_exist, num_of_wave, hp):
    noise_array = np.random.choice([True,False], size=num_of_wave, p=[prob_of_exist, 1-prob_of_exist])
    return(f"({convert_sequences_command(noise_array)}+{hp})")

def noise_command_existance_batch(prob_array,hp_array):
    tasks_todo_raw = []
    for prob in prob_array:
        for hp in hp_array:
            command_string = noise_array_generator_single_existance(prob, 300, hp)
            tasks_todo_raw.append(command_string)
    return tasks_todo_raw

def noise_array_generator_single_simple_gap(gap_size, num_of_wave, hp):
    noise_array = [False]*gap_size + [True]*(num_of_wave - gap_size)
    return(f"({convert_sequences_command(noise_array)}+{hp})")


def noise_command_simple_gap_batch(gap_array, hp_array):

    tasks_todo_raw = []
    for gap_size in gap_array:
        for hp in hp_array:
            command_string = noise_array_generator_single_simple_gap(gap_size, 800, hp)
            tasks_todo_raw.append(command_string)
    return tasks_todo_raw


def noise_array_generator_single_simple_regular_pulse(pulse_size, num_of_wave, hp):
    noise_array = [True]*pulse_size + [False]*(num_of_wave - pulse_size)
    return(f"({convert_sequences_command(noise_array)}+{hp})")

def noise_array_generator_regular_pulse_batch(pulse_array, hp_array):
    tasks_todo_raw = []
    for pulse_size in pulse_array:
        for hp in hp_array:
            command_string = noise_array_generator_single_simple_regular_pulse(pulse_size, 800, hp)
            tasks_todo_raw.append(command_string)
    return tasks_todo_raw




def closest_pico_time_per_sample(desired_ns):
    time_values = [
        '10ns', '20ns', '40ns', '80ns', '160ns', '320ns', '640ns',
        '1micro_s', '3micro_s', '5micro_s', '10micro_s', '20micro_s',
        '41micro_s', '82micro_s', '164micro_s', '328micro_s', '655micro_s',
        '1ms', '3ms', '5ms', '10ms'
    ]
    time_dict = {10 * 2**i: value for i, value in enumerate(time_values)}
    closest_key = min(time_dict.keys(), key=lambda x: abs(x - desired_ns))
    # Retrieve the corresponding value from the dictionary
    closest_value = time_dict[closest_key]
    return closest_value


def use_pico_and_record(sample_instruction):
    with Picoscope(time_per_sample=sample_instruction, probe_10x=True, trigger_channel='a') as scope:
        times, voltages_a, voltages_b = scope.get_trace(f'sampling at {sample_instruction}')
    return times, voltages_a, voltages_b




# automated
def tasks_execute(tasks_todo_np):
    ard_operation_time_ms = 3000
    num_of_tasks, _ = tasks_todo_np.shape
    times_array = np.zeros((num_of_tasks,8064))
    voltages_array_a = np.zeros_like(times_array)
    voltages_array_b = np.zeros_like(times_array)
    for tasks_number in range(num_of_tasks):
        tasks_single = tasks_todo_np[tasks_number]
        print(tasks_single)
        # getting the arduino to generate waves
        arduino_connect_and_send(instruction_generator(ard_operation_time_ms, tasks_single))
        # calculated the best time scale for sampling
        best_sample_ns = (tasks_single[0]/2)
        sample_instruction = closest_pico_time_per_sample(best_sample_ns)
        times, voltages_a, voltages_b = use_pico_and_record(sample_instruction)
        times_array[tasks_number] = times
        voltages_array_a[tasks_number] = voltages_a
        voltages_array_b[tasks_number] = voltages_b
        time.sleep(2)
    return times_array, voltages_array_a, voltages_array_b

# less automated
def tasks_execute_manual_sample_time(tasks_todo_np,sample_time):
    ard_operation_time_ms = 3000
    num_of_tasks, _ = tasks_todo_np.shape
    times_array = np.zeros((num_of_tasks,8064))
    voltages_array_a = np.zeros_like(times_array)
    voltages_array_b = np.zeros_like(times_array)
    for tasks_number in range(num_of_tasks):
        tasks_single = tasks_todo_np[tasks_number]
        print(tasks_single)
        # getting the arduino to generate waves
        arduino_connect_and_send(instruction_generator(ard_operation_time_ms, tasks_single))
        # calculated the best time scale for sampling
        best_sample_ns = sample_time
        sample_instruction = closest_pico_time_per_sample(best_sample_ns)
        times, voltages_a, voltages_b = use_pico_and_record(sample_instruction)
        times_array[tasks_number] = times
        voltages_array_a[tasks_number] = voltages_a
        voltages_array_b[tasks_number] = voltages_b
        time.sleep(2)
    return times_array, voltages_array_a, voltages_array_b


# very manual
def tasks_execute_raw_command_manual_sample_time(tasks_todo_np_raw,sample_time):
    # arduino will decide time this time
    #ard_operation_time_ms = 3000
    num_of_tasks = len(tasks_todo_np_raw)
    times_array = np.zeros((num_of_tasks,8064))
    voltages_array_a = np.zeros_like(times_array)
    voltages_array_b = np.zeros_like(times_array)
    for tasks_number in range(num_of_tasks):
        task_single_raw = tasks_todo_np_raw[tasks_number]
        print(task_single_raw)
        # getting the arduino to generate waves
        arduino_connect_and_send_wait_on_return(task_single_raw)
        # wait for long string to finish 
        # calculated the best time scale for sampling
        best_sample_ns = sample_time
        sample_instruction = closest_pico_time_per_sample(best_sample_ns)
        times, voltages_a, voltages_b = use_pico_and_record(sample_instruction)
        times_array[tasks_number] = times
        voltages_array_a[tasks_number] = voltages_a
        voltages_array_b[tasks_number] = voltages_b
        time.sleep(2)
    return times_array, voltages_array_a, voltages_array_b



