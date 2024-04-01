import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
from matplotlib import rc

rc('font',**{'family':'serif','serif':['Times']})
rc('text', usetex=True)
rc('font', size=14)

bpf_programs = {
    'tracex5': [228, 152, 152, 56],
    'trace_event': [700],
    'syscall_tp': [132,132,132,132],
    'bmc': [524, 864, 984, 1476, 716, 376, 640]
}
rust_programs = {
    'tracex5': [0x380, 0x179, 0x68, 0x148],
    'trace_event': [0x0004c8, 0x0001a3, 0x0000d0, 0x000170],
    'syscall_tp': [0x000380,0x000140,0x000048,0x000148],
    'bmc': [0x000750, 0x001000, 0xc4b, 0x0002a8, 0x000338]
}
# The adding represents the individual bpf program sizes
bpf_programs_new = {
    'tracex5': [233 + 160 + 158 + 64],
    'trace_event': [768],
    'syscall_tp': [138 + 138 + 138 + 138],
    'bmc': [532 + 823 + 1010, 1425 + 667 + 356 + 566]
}
page_size = 4096

# Plotting
fig, ax = plt.subplots()

bar_width = 0.20
pair_gap = 0.0
group_gap = 1.0

xticks = []

for group_index, name in enumerate(bpf_programs.keys()):
    # Calculate the used and unused space for BPF programs
    used_bpf = sum(bpf_programs[name])
    unused_bpf = len(bpf_programs[name]) * page_size - used_bpf
    
    # Calculate the used and unused space for Rust programs
    rust_sizes_dec = [size for size in rust_programs.get(name, [])]
    used_rust = sum(rust_sizes_dec)
    unused_rust = len(rust_sizes_dec) * page_size - used_rust
    
    # Calculate the used and unused space for the new BPF programs
    used_bpf_new = sum(bpf_programs_new[name])
    unused_bpf_new = len(bpf_programs_new[name]) * page_size - used_bpf_new
    
    # Determine bar positions
    bpf_new_position = group_index * (3 * bar_width + 2 * pair_gap + group_gap)
    bpf_position = bpf_new_position + bar_width + pair_gap
    rust_position = bpf_position + bar_width + pair_gap

    # Plot BPF used and unused space
    ax.bar(bpf_position, used_bpf, width=bar_width, color='tab:blue', align='edge', label='BPF')
    ax.bar(bpf_position, unused_bpf, bottom=used_bpf, width=bar_width, color='tab:blue', align='edge', alpha = .3)
    
    # Plot Rust used and unused space, if present
    ax.bar(rust_position, used_rust, width=bar_width, color='tab:green', align='edge', label='REX')
    ax.bar(rust_position, unused_rust, bottom=used_rust, width=bar_width, color='tab:green', align='edge', alpha = .3)
    
    # Plot new BPF used and unused space
    ax.bar(bpf_new_position, used_bpf_new, width=bar_width, color='tab:orange', align='edge', label='BPF Packed')
    ax.bar(bpf_new_position, unused_bpf_new, bottom=used_bpf_new, width=bar_width, color='tab:orange', align='edge', alpha = .3)
    
    # Add midpoint for xticks
    xticks.append((rust_position + bpf_position) / 2)

# Labels and formatting
ax.set_ylabel('Bytes')
ax.set_xticks(xticks)
ax.set_xticklabels(bpf_programs.keys())

# Simplified legend
ax.legend(handles=[
    mpatches.Patch(color='tab:blue', label='BPF'),
    mpatches.Patch(color='tab:green', label='REX'),
    mpatches.Patch(color='tab:orange', label='BPF Packed'),
], loc='upper left')

sec_ax = ax.secondary_yaxis('right', functions=(lambda x: x / page_size, lambda x: x * page_size))
sec_ax.set_ylabel('Number of Pages')
sec_ax.set_ylim(ax.get_ylim())

# ax.set_xticklabels(ax.get_xticklabels(), size='large')
# ax.set_yticklabels(ax.get_yticklabels(), size='large')
# sec_ax.set_yticklabels(sec_ax.get_yticklabels(), size='large')

# ax.legend(loc='upper left', fontsize='small')

plt.tight_layout()
plt.show()
plt.savefig("mem.pdf", bbox_inches="tight")