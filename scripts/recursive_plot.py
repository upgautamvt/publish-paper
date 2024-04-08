import csv

from matplotlib import rc
import matplotlib.pyplot as plt
import numpy as np
import os


def read_data(folder_path: str, prog_type: str) -> dict:
    all_data = {}
    for i in range(0, 33):
        filename = prog_type + str(i)
        # print(filename)
        file_path = os.path.join(folder_path, filename)
        # Check if it is a file
        if os.path.isfile(file_path):
            with open(file_path, "r") as file:
                col = []
                for line in file:
                    col.append(int(line.strip()))
                all_data[i] = np.average(np.array(col))
    return all_data


# NOTE: don't change

rc("font", **{"family": "serif", "serif": ["Times"]})
rc("text", usetex=True)

bpf_data = read_data("./recursive_bench/", "bpf_")
rust_data = read_data("./recursive_bench/", "rust_")

sorted_keys = sorted(bpf_data.keys())
sorted_bpf = [bpf_data[key] for key in sorted_keys]
sorted_rust = [rust_data[key] for key in sorted_keys]
max_val = max(*sorted_bpf, *sorted_rust)

recursive_results = {
    "BPF tail call": sorted_bpf,
    "Rust function call": sorted_rust,
}


# NOTE: don't change
with plt.style.context("seaborn-v0_8-paper"):
    x = np.arange(len(sorted_keys))  # the label locations
    width = 0.25  # the width of the bars
    multiplier = 0
    y = np.arange(0, max_val, 0.2)

    # NOTE: don't change
    fig, ax = plt.subplots(layout="tight")
    # fig.set_size_inches(8, 4.8) # for slides
    fig.set_size_inches(4.5, 2.7)

    for setup, time_consume in recursive_results.items():
        # offset = width * multiplier
        # NOTE: change to plot
        rects = ax.plot(
            sorted_keys,
            time_consume,
            label=setup,
        )
        print("time_consume")
        # multiplier += 1

    y_min, y_max = ax.get_ylim()
    ax.set_ylim(y_min, y_max * 1.12)
    y = np.arange(y_min, y_max, 0.2)

    # Add some text for labels, title and custom x-axis tick labels, etc.
    # NOTE: size=large
    ax.set_xlabel(r"\# of stack depth", size="large")
    ax.set_ylabel("Run Time (ns)", size="large")
    # ax.set_xticks(x + width, x + 1)
    # ax.set_xticklabels(ax.get_xticklabels(), size="large")
    # ax.set_yticks(y, list(map(lambda x: "%.1f" % x, y)))
    # ax.set_yticklabels(ax.get_yticklabels(), size="large")
    ax.legend(loc="upper left", ncols=3, fontsize="small")

    # NOTE: don't change
    plt.savefig("./recursive.pdf", bbox_inches="tight")
    plt.close()
