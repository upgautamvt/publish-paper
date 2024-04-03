import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
from matplotlib import rc

rc('font',**{'family':'serif','serif':['Times']})
rc('text', usetex=True)
# rc('font', size=14)

bpf_programs = {
    'tracex5': [228, 152, 152, 56],
    'trace_event': [700],
    'syscall_tp': [132,132,132,132],
    'BMC': [524, 864, 984, 1476, 716, 376, 640]
}
rust_programs = {
    'tracex5': [0x380, 0x179, 0x68, 0x148],
    'trace_event': [0x0004c8, 0x0001a3, 0x0000d0, 0x000170],
    'syscall_tp': [0x000380,0x000140,0x000048,0x000148],
    'BMC': [0x000750, 0x001000, 0xc4b, 0x0002a8, 0x000338]
}
# The adding represents the individual bpf program sizes
bpf_programs_new = {
    'tracex5': [233 + 160 + 158 + 64],
    'trace_event': [768],
    'syscall_tp': [138 + 138 + 138 + 138],
    'BMC': [532 + 823 + 1010, 1425 + 667 + 356 + 566]
}
page_size = 4096

bar_width = 0.20
pair_gap = 0.0
group_gap = 1.0

xticks = []

def process_one_category(data):
    used = np.array(list(map(sum, data.values())))
    unused = np.array(list(map(lambda x: len(x) * page_size,
                          data.values()))) - used
    return used, unused

data = {
    'BPF-packed': process_one_category(bpf_programs_new),
    'BPF': process_one_category(bpf_programs),
    'REX': process_one_category(rust_programs)
}

with plt.style.context('seaborn-v0_8-paper'):
    x = np.arange(len(bpf_programs))
    width = bar_width
    multiplier = 0

    fig, ax = plt.subplots(layout='tight')
    fig.set_size_inches(4.5, 2.7)

    for cat, (used, unused) in data.items():
        offset = width * multiplier
        rects = ax.bar(x + offset, used, width, label='%s occupied' % cat)
        # same color but with alpha=0.5
        c = (*rects.patches[0]._facecolor[:-1], 0.4)
        ax.bar(x + offset, unused, width, bottom=used, color=c, label='%s empty' % cat)
        multiplier += 1

    # Labels and formatting
    ax.set_xticks(x + width, x + 1)
    ax.set_xticklabels(bpf_programs.keys(), size='large')

    y_min, y_max = ax.get_ylim()
    y = np.arange(y_min, y_max, 5000)
    ax.set_yticks(y, list(map(lambda x: '%d' % (x // 1000), y)))
    ax.set_ylabel('KBs', size='large')
    ax.set_yticklabels(ax.get_yticklabels(), size='large')

    # Somehow secondary_yaxis does not work well with set_yticks and
    # set_yticklabels
    #sec_ax = ax.secondary_yaxis('right', functions=(lambda x: x / page_size,
    #                                                lambda x: x * page_size))
    #sec_ax.set_ylabel('Number of Pages', size='large')
    #sec_ax.set_ylim(np.array(ax.get_ylim()) / page_size)
    #sec_ax.set_yticks(sec_ax.get_yticks())
    #sec_ax.set_yticklabels(sec_ax.get_yticklabels(), size='large')

    sec_ax = ax.twinx()
    sec_ax.set_ylabel('Number of Pages', size='large')
    sec_ax.set_ylim(ax.get_ylim())
    sec_ax_yticks = np.arange(*sec_ax.get_ylim(), page_size).astype(np.int64)
    sec_ax.set_yticks(sec_ax_yticks)
    sec_ax.set_yticklabels(list(map(str, sec_ax_yticks // page_size)),
                           size='large')


    ax.legend(loc='upper left', ncols=2, fontsize='small')

    plt.tight_layout()
    # plt.show()
    plt.savefig("mem.pdf", bbox_inches="tight")