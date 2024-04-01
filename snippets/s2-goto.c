  if (likely(l4policy && !l4policy->wildcard_dport)) {
    *match_type = POLICY_MATCH_L4_ONLY;
-   policy = l4policy;
-   goto policy_check_entry;
+   return __account_and_check(ctx, l4policy, ...);
  }

  if (likely(policy && !policy->wildcard_protocol)) {
    *match_type = POLICY_MATCH_L3_PROTO;
-   goto policy_check_entry;
+   return __account_and_check(ctx, policy, ...);
  }

