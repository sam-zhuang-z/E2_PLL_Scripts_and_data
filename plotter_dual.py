# auto loader script for mass plot generation and batch inspection 
from matplotlib import pyplot as plt
import numpy as np
from os import listdir 
from os import makedirs
from tqdm import tqdm
target_dir = "/home/samz/programming/E2/data_collection/simple_existance_longer_sample"
target_dir = "/home/samz/programming/E2/data_collection/simple_gap_80ns"
target_dir = "/home/samz/programming/E2/data_collection/simple_gap_800waves_320ns/"
#target_dir = "/home/samz/programming/E2/data_collection/simple_gap_very_long/"
#target_dir = "/home/samz/programming/E2/data_collection/comp2_expo_measurement_21phase/"
#target_dir = "/home/samz/programming/E2/data_collection/comp2_expo_measurement_7phase/"
#target_dir = "/home/samz/programming/E2/data_collection/sec_8_locking_behaviour_100k_100k_1000pf_100k_3300pf/"
#target_dir = "/home/samz/programming/E2/data_collection/sec_8_locking_behaviour_100k_100k_1000pf_100k_3300pf_capB/"
#target_dir = "/home/samz/programming/E2/data_collection/sec_8_locking_behaviour_100k_100k_1000pf_100k_3300pf_comp2_out"

files = listdir(target_dir)
npy_files = [file for file in files if file.endswith(".npy")]
#time_files = [file for file in npy_files if "time" in file]

# shape determination of designated files
to_be_plotted = []
exp_details = []
N_exp = 0
for file_names in npy_files:
    shape_determinator = np.load(f"{target_dir}/{file_names}")
    if shape_determinator.ndim == 2:
        N_exp, data_points = shape_determinator.shape
        if data_points == 8064:
            to_be_plotted.append(file_names)
        else:
            exp_details.append(file_names)
    else:
        exp_details.append(file_names)
#
#

time_files = [file for file in to_be_plotted if "time" in file]
to_be_plotted.remove(time_files[0])


#### user customization options
to_be_plotted_smaller_1 = []
for plot_options in to_be_plotted:
    keep_status = input(f"keepthis:({plot_options})?  (y/n)")
    if keep_status == "y":
        to_be_plotted_smaller_1.append(plot_options)
    else:
        pass

to_be_plotted_smaller_2 = []
for plot_options in to_be_plotted:
    keep_status = input(f"keepthis:({plot_options})?  (y/n)")
    if keep_status == "y":
        to_be_plotted_smaller_2.append(plot_options)
    else:
        pass


#####
# start plotting 
# loop for each N 
# loading the data_points into arrays
times_np = np.load(f"{target_dir}/{time_files[0]}")
exp_detes = np.load(f"{target_dir}/{exp_details[0]}")
data_set_size_1 = len(to_be_plotted_smaller_1)
data_set_size_2 = len(to_be_plotted_smaller_2)
data_set_3d_1 = np.zeros((data_set_size_1,N_exp,8064))
data_set_3d_2 = np.zeros((data_set_size_2,N_exp,8064))
for i in range(data_set_size_1):
    data_set_3d_1[i] = np.load(f"{target_dir}/{to_be_plotted_smaller_1[i]}")
    print(f"loaded {target_dir}/{to_be_plotted_smaller_1[i]}")
for i in range(data_set_size_2):
    data_set_3d_2[i] = np.load(f"{target_dir}/{to_be_plotted_smaller_2[i]}")
    print(f"loaded {target_dir}/{to_be_plotted_smaller_2[i]}")


for N in tqdm(range(N_exp)):
    fig = plt.figure()
    ax1 = fig.add_subplot(2, 1, 1)
    ax2 = fig.add_subplot(2, 1, 2)
    for i in range(data_set_size_1):
        plt.ylim(-1,6)
        ax1.plot(times_np[N],data_set_3d_1[i][N], label=to_be_plotted_smaller_1[i], linewidth=0.4)
        ax1.legend(loc='upper right', fontsize = 8)
        ax1.set_ylabel("SIG_IN and VCO output/V")

    for i in range(data_set_size_2):
        plt.ylim(-1,6)
        ax2.plot(times_np[N],data_set_3d_2[i][N], label=to_be_plotted_smaller_2[i], linewidth=0.4)
        ax2.legend(loc='upper right', fontsize = 8)
        ax2.set_xlabel("time/s")
        ax2.set_ylabel("vco_output/V")
    makedirs(f"{target_dir}/dual_plots", exist_ok=True)
    fig.savefig(f"{target_dir}/dual_plots/{exp_detes[N]}.png", dpi = 500)
    plt.close(fig)
        
# for elements in to be plotted array 
    # load numpy objects
    # plot with label(generated from file name)
# save the graph is sub directory with 


