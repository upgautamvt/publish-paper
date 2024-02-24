static __always_inline void *
ctx_data (const struct __sk_buff *ctx)
{
  void *ptr;
  asm volatile (
    "%0 = *(u32 *)(%1 + %2)"
    : "=r"(ptr)
    : "r"(ctx),
      "i"(offsetof (struct __sk_buff, data))
  );
  return ptr;
}
