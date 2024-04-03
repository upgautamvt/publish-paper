...
switch (len) {
  case 96: __it_mob(d, s, 64); fallthrough;
  case 88: jmp_88: __it_mob(d, s, 64); fallthrough;
  ...
  break;
  case 94: __it_mob(d, s, 16); __it_mob(d, s, 32); goto jmp_88;
  case 86: __it_mob(d, s, 16); __it_mob(d, s, 32); goto jmp_80;
  ...
  break;
  case 92: __it_mob(d, s, 32); goto jmp_88;
  case 84: __it_mob(d, s, 32); goto jmp_80;
  ...
  break;
  case 90: __it_mob(d, s, 16); goto jmp_88;
  case 82: __it_mob(d, s, 16); goto jmp_80;
  ...
    break;
  case  1: __it_mob(d, s, 8);
    break;
...
