+  skb->cb[0] = MARK_MAGIC_TO_PROXY | (proxy_port << 16);
  if (!revalidate_data(skb, &data, &data_end, &ip4))
  	return DROP_INVALID;
  ret = ipv4_l3(skb, ETH_HLEN, (__u8 *) &router_mac, (__u8 *) &host_mac, ip4);
  if (IS_ERR(ret))
  	return ret;
-  skb->cb[0] = MARK_MAGIC_TO_PROXY | proxy_port << 16;
