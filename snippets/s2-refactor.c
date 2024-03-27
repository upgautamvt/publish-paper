  static __always_inline int
  ipv4_ct_extract_l4_ports(...)
  {
  #ifdef ENABLE_IPV4_FRAGMENTS
  ...
- if (unlikely(ipv4_is_fragment(ip4)))
-   return ipv4_handle_fragment(...)
- #endif
+   return ipv4_handle_fragmentation(...)
+ #else
  /* load sport + dport into tuple */
  if (ctx_load_bytes(ctx, off, &tuple->dport, 4) < 0)
    return DROP_CT_INVALID_HDR;
+ #endif
    return CTX_ACT_OK;
  }