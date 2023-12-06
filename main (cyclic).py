import numpy as np
from numpy.polynomial import Polynomial


def cyclic_encode(bits):
  main_pol = np.array(bits+[0,0,0])
  gen_pol = np.array([1, 0, 1, 1])
  ost = np.polydiv(main_pol, gen_pol)[1]
  ost = list(map(lambda x: int(x%2), ost))
  return bits + ost


org = "0010"
org_trans = list(map(int,list(org)))
encoded_data = cyclic_encode(org_trans)
print(encoded_data)
encoded_data = np.array(encoded_data)
gen_pol = np.array([1, 0, 1, 1])



error_dict = {}
for i in range(1,128):
  error = bin(i)[2:].zfill(7)
  noise_data = []
  for j in range(7):
    if error[j] == '0':
      noise_data.append(encoded_data[j])
    else:
      noise_data.append(1-encoded_data[j])
  noise_data = np.array(noise_data)
  syndrome = np.polydiv(noise_data, gen_pol)[1]
  syndrome = list(filter(lambda x: x%2, syndrome))
  if error_dict.get(error.count('1')) is not None:
    error_dict[error.count('1')][0] += bool(syndrome)
    error_dict[error.count('1')][1] += 1
  else:
    error_dict[error.count('1')] = [int(bool(syndrome)),1]

for k,v in error_dict.items():
  print(f'Кратность ошибки {k}   Кол-во обнаруженных ошибок {v[0]} Кол-во ошибок данной кратности  {v[1]}')
