import numpy as np



with open("output_bpf_ns2") as f:
    content = f.readlines()
    arr = np.array(list(map(lambda x : int(x.strip()), content)))
    mean = np.mean(arr)
    std = np.std(arr)
    print(f"ebpf mean: { mean } std: { std }")
with open("output_rust_ns2") as f:
    content = f.readlines()
    arr = np.array(list(map(lambda x : int(x.strip()), content)))
    mean = np.mean(arr)
    std = np.std(arr)
    print(f"rust mean: { mean } std: { std }")
