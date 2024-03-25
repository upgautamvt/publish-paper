import numpy as np

def compute_stats(filename):
    with open(filename) as f:
        content = f.readlines()
    arr = np.array(list(map(lambda x: int(x.strip().split()[-1]), content)))
    return np.mean(arr), np.std(arr)

print('bpf: ', *compute_stats('bpf_startup.txt'))
print('rex: ', *compute_stats('rex_startup.txt'))
