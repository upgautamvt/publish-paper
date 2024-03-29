let set_iter = payload
    .windows(4)
    .enumerate()
    .filter_map(|(i, v)| 
      if v == b"set " { Some(i) } else { None }
    );
for index in set_iter {
  ...
  payload
    .iter()
    .take_while(|&&c| c != b' ')
    .for_each(|&c| {
    ...
  });
  ...
}