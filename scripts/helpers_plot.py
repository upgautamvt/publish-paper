import numpy as np
import matplotlib.pyplot as plt
import csv
from collections import defaultdict
from matplotlib import rc

rc('font',**{'family':'serif','serif':['Times']})
rc('text', usetex=True)
# plt.rcParams.update({'font.size': 11})

def process_data(filename, outlier=2000):
    all_elapsed_times = defaultdict(list)
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            map_type = row[0]  # The first element is map_type
            elapsed_times = [float(time) for time in row[1:] if float(time) <= outlier]
            all_elapsed_times[map_type].append(elapsed_times)
    
    stats = {}
    for map_type, combined_times in all_elapsed_times.items():
        combined_times_flat = np.concatenate(combined_times)
        mean_elapsed_time = np.mean(combined_times_flat)
        std_dev_elapsed_time = np.std(combined_times_flat, ddof=1)  # Using ddof=1 for sample standard deviation
        n = len(combined_times_flat)
        # stderr_elapsed_time = std_dev_elapsed_time / np.sqrt(n)
        stats[map_type] = (mean_elapsed_time, std_dev_elapsed_time, std_dev_elapsed_time)

    return stats

# Generalized processing for any number of files
file_names = ['rex_times.csv', 'v5.15.19-times.csv']
all_stats = [process_data(f"helpers_benchmark/{file}") for file in file_names]

# Plotting
with plt.style.context('seaborn-v0_8-paper'):

    fig, ax = plt.subplots(layout='tight')
    fig.set_size_inches(4.5, 2.7)

    
    # Sorting map types in alphabetical order
    map_types = sorted(set([key for stats in all_stats for key in stats.keys()]))

    bar_width = 0.3
    index = np.arange(len(map_types))

    labels = ['REX', 'eBPF']

    for i, stats in enumerate(all_stats):
        means = [stats[map_type][0] if map_type in stats else 0 for map_type in map_types]
        stderrs = [stats[map_type][2] if map_type in stats else 0 for map_type in map_types]
        
        plt.bar(index + i * bar_width, means, bar_width, yerr=stderrs, alpha=1.0, label=labels[i], error_kw={'elinewidth': 0.6, 'capsize': 3, 'markeredgewidth': 0.6})

    # plt.xlabel('Map Type', size='large')
    plt.ylabel('Mean Elapsed Time (ns)', size='large')
    plt.xticks(index + bar_width/2, map_types, size='small', rotation=45, ha='right')
    plt.yticks(size='large')
    plt.legend(loc='upper left')


    plt.tight_layout()
    # plt.show()
    plt.savefig("helpers.pdf", bbox_inches="tight")
