#[repr(C)]
pub struct RexMap<const MT: bpf_map_type, K, V> {
  map_type: bpf_map_type,
  key_size: u32,
  val_size: u32,
  max_size: u32,
  map_flag: u32,
  pub(crate) kptr: *mut (),
  ...
}

impl<const MT: bpf_map_type, K, V> RexMap<MT, K, V> {
  pub const fn new(size: u32, flag: u32) -> RexMap<MT, K, V> {
    ...
  }
}

pub type RexArrayMap<V> = RexMap<BPF_MAP_TYPE_ARRAY, u32, V>;
pub type RexHashMap<K, V> = RexMap<BPF_MAP_TYPE_HASH, K, V>;

pub(crate) fn map_lookup_elem<const MT: bpf_map_type, K, V>(
  map: &IUMap<MT, K, V>,
  key: &K,
) -> Option<&mut V> {
  let kp = unsafe { core::ptr::read_volatile(&map.kptr) };
  if unlikely(map_kptr.is_null()) {
    return None;
  }
  let value = unsafe {
    stub::bpf_map_lookup_elem(kp, key as *const K as *const ())
      as *mut V
  };
  if value.is_null() {
    None
  } else {
    Some(unsafe { &mut *value })
  }
}