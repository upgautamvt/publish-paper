#ifdef ENABLE_SRV6_SRH_ENCAP
  case NEXTHDR_ROUTING: {
  ...
    switch (srh->rthdr.nexthdr) {
    case IPPROTO_IPIP:
      goto parse_outer_ipv4;
    case IPPROTO_IPV6:
      goto parse_outer_ipv6;
    default:
      return DROP_INVALID;
    }
  }
#endif /* ENABLE_SRV6_SRH_ENCAP */
