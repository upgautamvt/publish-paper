#pragma clang loop unroll(disable)
for (unsigned int off = 0;
  off < BMC_MAX_PACKET_LENGTH && payload + off + 1 <= data_end;
  off++) {
  if (set_found == 0 && payload[off] == 's' &&
      payload + off + 3 <= data_end &&
      payload[off + 1] == 'e' && payload[off + 2] == 't') {
    ...
    set_found = 1;
  } else if (key_found == 0 && set_found == 1 &&
             payload[off] != ' ') {
    if (payload[off] == '\r') {
      set_found = 0;
      key_found = 0;
    } else {
      ...
      key_found = 1;
    }
  } else if (key_found == 1) {
    if (payload[off] == ' ') {
      ...
      set_found = 0;
      key_found = 0;
    } else {
      ...
    }
  }
}
