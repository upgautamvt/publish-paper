#ifndef ENABLE_SKIP_FIB
    ...
if (likely(ret == BPF_FIB_LKUP_RET_NO_NEIGH)) {
  nh_params.nh_family = fib_params->l.family;
    ...
} else {
  return DROP_NO_FIB;
}
...
skip_oif:
#else
*oif = DIRECT_ROUTING_DEV_IFINDEX;
-nh_params.nh_family = fib_params->l.family;
#endif /* ENABLE_SKIP_FIB */
...
-dmac = nh_params.nh_family == AF_INET ?
+dmac = fib_params->l.family == AF_INET ?
            ...
