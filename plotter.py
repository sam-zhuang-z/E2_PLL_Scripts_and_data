# auto loader script for mass plot generation and batch inspection 
from matplotlib import pyplot as plt
import numpy as np
from os import listdir 
from os import makedirs
from tqdm import tqdm
target_dir = "/home/samz/programming/E2/data_collection/simple_existance_longer_sample"
target_dir = "/home/samz/programming/E2/data_collection/simple_gap_80ns"
target_dir = "/home/samz/programming/E2/data_collection/simple_gap_800waves_320ns/"
target_dir = "/home/samz/programming/E2/data_collection/simple_gap_very_long/"
target_dir = "/home/samz/programming/E2/data_collection/simple_existance_with_seed/"
target_dir = "/home/samz/programming/E2/data_collection/comp1_expo_measurement_7phase/"

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
to_be_plotted_smaller = []
for plot_options in to_be_plotted:
    keep_status = input(f"keepthis:({plot_options})?  (y/n)")
    if keep_status == "y":
        to_be_plotted_smaller.append(plot_options)
    else:
        pass
to_be_plotted = to_be_plotted_smaller
#####
# start plotting 
# loop for each N 
# loading the data_points into arrays
times_np = np.load(f"{target_dir}/{time_files[0]}")
exp_detes = np.load(f"{target_dir}/{exp_details[0]}")
data_set_size = len(to_be_plotted)
data_set_3d = np.zeros((data_set_size,N_exp,8064))
for i in range(data_set_size):
    data_set_3d[i] = np.load(f"{target_dir}/{to_be_plotted[i]}")
    print(f"loaded {target_dir}/{to_be_plotted[i]}")
print(exp_detes)
for N in tqdm(range(N_exp)):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    for i in range(data_set_size):
        ax.plot(times_np[N],data_set_3d[i][N], label=to_be_plotted[i], markersize = 2, linewidth=0.5)
        plt.ylim(-1,6)
        ax.legend(loc='upper right', fontsize = 10)
        ax.set_ylabel("signal voltage/V")
        ax.set_xlabel("time/s")
    makedirs(f"{target_dir}/plots", exist_ok=True)
    fig.savefig(f"{target_dir}/plots/{exp_detes[N]}.png", dpi = 500)
    plt.close(fig)
        
# for elements in to be plotted array 
    # load numpy objects
    # plot with label(generated from file name)
# save the graph is sub directory with 


