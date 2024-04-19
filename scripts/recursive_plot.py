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
                all_data[i] = np.average(np.array(col[5:])) # dry-run 5 rounds
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
    "eBPF tail call": (sorted_bpf, '.-'),
    "Rex recursive fn call": (sorted_rust, 's-'),
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
    fig.set_size_inches(4.5, 2)

    # for setup, time_consume in recursive_results.items():
        # offset = width * multiplier
        # NOTE: change to plot
    ax.plot(sorted_keys, sorted_bpf, label="eBPF tail call", marker='o', mew=0.1, markersize=4)
    ax.plot(sorted_keys, sorted_rust, label="Rex recursive fn call", marker='^', mew=0.1, markersize=4)
        # print("time_consume")
        # multiplier += 1

    x = np.arange(sorted_keys[0], sorted_keys[-1], 5).astype(np.int64)
    y_min, y_max = ax.get_ylim()
    # ax.set_ylim(y_min, y_max * 1.12)
    y = np.arange(0, y_max + 100, 100).astype(np.int64)

    # Add some text for labels, title and custom x-axis tick labels, etc.
    # NOTE: size=large
    ax.set_xlabel("Call depth", size="large")
    ax.set_ylabel("Runtime (ns)", size="large")
    ax.set_xticks(x)
    ax.set_xticklabels(ax.get_xticklabels(), size="large")
    ax.set_yticks(y)
    ax.set_yticklabels(ax.get_yticklabels(), size="large")
    ax.legend(loc="upper left", ncols=1, fontsize="small")

    # NOTE: don't change
    plt.savefig("./recursive.pdf", bbox_inches="tight")
