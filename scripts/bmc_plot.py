import csv

import matplotlib.pyplot as plt
import numpy as np

from matplotlib import rc
rc('font',**{'family':'serif','serif':['Times']})
rc('text', usetex=True)

with open('bmc-results.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)

    data = [row for row in reader][1:]
    nr_cpu = [float(row[0]) for row in data]
    vanilla = [float(row[1]) for row in data]
    bpf = [float(row[2]) for row in data]
    rust = [float(row[3]) for row in data]
    vanilla_stdev = [float(row[4]) for row in data]
    bpf_stdev = [float(row[5]) for row in data]
    rust_stdev = [float(row[6]) for row in data]

max_val = max(*vanilla, *bpf, *rust) / 1000000

bmc_results = {
    'MemcachedSR': np.array(vanilla) / 1000000,
    'eBPF-BMC': np.array(bpf) / 1000000,
    'Rex-BMC': np.array(rust) / 1000000,
}

bmc_results_stdev = {
    'MemcachedSR': np.array(vanilla_stdev) / 1000000,
    'eBPF-BMC': np.array(bpf_stdev) / 1000000,
    'Rex-BMC': np.array(rust_stdev) / 1000000,
}

with plt.style.context('seaborn-v0_8-paper'):
    x = np.arange(len(data))  # the label locations
    width = 0.25  # the width of the bars
    multiplier = 0
    y = np.arange(0, max_val, 0.2)

    fig, ax = plt.subplots(layout='tight')
    # fig.set_size_inches(8, 4.8) # for slides
    fig.set_size_inches(4.5, 2.7)

    for setup, throughput in bmc_results.items():
        offset = width * multiplier
        rects = ax.bar(x + offset, throughput, width, label=setup,
                       yerr=bmc_results_stdev[setup], capsize=1,
                       error_kw={"elinewidth": 0.6, "mew": 0.6})
        multiplier += 1

    y_min, y_max = ax.get_ylim()
    ax.set_ylim(y_min, y_max * 1.12)
    y = np.arange(y_min, y_max, 0.2)

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_xlabel(r'\# of cores', size='large')
    ax.set_ylabel('Throughput\n(MReq/s)', size='large')
    ax.set_xticks(x + width, x + 1)
    ax.set_xticklabels(ax.get_xticklabels(), size='large')
    ax.set_yticks(y, list(map(lambda x: '%.1f' % x, y)))
    ax.set_yticklabels(ax.get_yticklabels(), size='large')
    ax.legend(loc='upper left', ncols=3, fontsize='small')

    plt.savefig("bmc.pdf", bbox_inches="tight")
