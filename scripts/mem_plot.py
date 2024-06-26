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
# Without rust termination
rust_programs = {
    'tracex5': [0x380, 0x179, 0x68, 0x148],
    'trace_event': [0x0004c8, 0x0001a3, 0x0000d0, 0x000170],
    'syscall_tp': [0x000380,0x000140,0x000048,0x000148],
    'BMC': [0x000750, 0x001000, 0xc4b, 0x0002a8, 0x000338]
}

# With rust termination branch
# rust_programs = {
#     'tracex5': [0x588, 0x869, 0x208, 0x1f8],
#     'trace_event': [0x6a8, 0x934, 0x268, 0x220],
#     'syscall_tp': [0x598,0x878,0x1e8,0x200],
#     'BMC': [0x7c8, 0x1000, 0xff3, 0x2c8, 0x358]
# }

# The adding represents the individual bpf program sizes
bpf_programs_new = {
    'tracex5': [233 + 160 + 158 + 64],
    'trace_event': [768],
    'syscall_tp': [138 + 138 + 138 + 138],
    'BMC': [532 + 823 + 1010, 1425 + 667 + 356 + 566]
}
bpf_bytecode_sizes = {
    'bpf': {
        'tracex5': 840,
        'trace_event': 1168,
        'syscall_tp': 768,
        'BMC': 8584
    },
    'bpf_packed': {
        'tracex5': 272+248+240+80,
        'trace_event': 1168,
        'syscall_tp': 240*4,
        'BMC': 656+1192+1392+2568+1144+416+976
    }
}
page_size = 4096

bar_width = 0.20

hatch_bpf_unused = '\\\\'
hatch_bpf_bytecode = '//'
edge_color_graphs = 'black'

xticks = []

def process_one_category(data, bytecode_sizes):
    used = np.array(list(map(sum, data.values())))
    bytecode = np.maximum(np.array([bytecode_sizes.get(name, 0) for name in data.keys()]), 0)
    unused = np.maximum(np.array(list(map(lambda x: len(x) * page_size, data.values()))) - used, 0)
    return used, unused, bytecode

# Data processing
data = {
    'BPF': process_one_category(bpf_programs, bpf_bytecode_sizes['bpf']),
    'BPF-Packed': process_one_category(bpf_programs_new, bpf_bytecode_sizes['bpf_packed']),
    'Rex': process_one_category(rust_programs, {})
}

print(data)

with plt.style.context('seaborn-v0_8-paper'):
    x = np.arange(len(bpf_programs))
    width = bar_width
    multiplier = 0

    fig, ax = plt.subplots(layout='tight')
    fig.set_size_inches(4.5, 2.7)

    colors = {}

    for cat, (used, unused, bytecode) in data.items():
        offset = width * multiplier

        rects = ax.bar(x + offset, used, width, label='%s' % cat)

        c = (*rects.patches[0]._facecolor[:-1], 1.0)
        colors[cat] = c
        ax.bar(x + offset, bytecode, width, bottom=used, hatch='//', edgecolor='black', linewidth=0, color=c, alpha=0.7)

        c = (*rects.patches[0]._facecolor[:-1], 1.0)
        ax.bar(x + offset, unused, width, bottom=used+bytecode, hatch='\\\\', edgecolor='black', linewidth=0, color=c, alpha=0.3)

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


    # ax.legend(loc='upper left', ncols=2, fontsize='small')

    ax.legend(handles=[
        mpatches.Patch(color=colors['BPF'], label='BPF'),
        mpatches.Patch(color=colors['BPF-Packed'], label='BPF-Packed'),
        mpatches.Patch(color=colors['Rex'], label='Rex'),
        mpatches.Patch(fill=False, hatch=hatch_bpf_bytecode, edgecolor=edge_color_graphs, color='black', label='Bytecode'),
        mpatches.Patch(fill=False, hatch=hatch_bpf_unused, edgecolor=edge_color_graphs,  color='dimgray', label='Unused Space'),
    ], loc='upper left', fontsize='small', ncols=2)

    plt.tight_layout()
    # plt.show()
    plt.savefig("mem.pdf", bbox_inches="tight")