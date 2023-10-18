import numpy as np
import matplotlib.pyplot as plt
import adi
import time

sdr = adi.Pluto("ip:192.168.2.1")

frequency = 2300e6+(2e6*2)
sdr.rx_lo = int(frequency)
sdr.tx_lo = int(frequency)

sdr.rx_buffer_size = 1000
sdr.sample_rate = 1e6


fio = 'pushnitsa'
encoded_bytes = fio.encode('ascii')
# Преобразование байтов в массив битов
bit_array = []
for byte in encoded_bytes:
    bits = bin(byte)[2:].zfill(8)  # Преобразование в биты
    bit_array.extend([int(bit) for bit in bits])
bit_start = np.ones(20)
bit_stop = np.ones(10)

print(len(bit_array))


bit_array_list = list(bit_array)
bit_array_list = list(bit_start) + bit_array_list + list(bit_stop)
bit_array = np.array(bit_array_list)
print(len(bit_array))

#sample = np.zeros(1024)
sample = np.zeros(len(bit_array)*200, dtype=complex)

for i in range(len(bit_array)):
    for o in range(100):
        if bit_array[i] == 1:
            sample[i * 100 + o] = 1 * 2 ** 14 + 1j * 2 ** 14
        elif bit_array[i] == 0:
            sample[i * 100 + o] = 1 * 2 ** 1 + 1j * 2 ** 1

rx = []

#sdr.tx(sample)
#sdr.tx_cyclic_buffer = True
for i in range(1000):
    if (i==200):
       sdr.tx(sample) 
    new_data = sdr.rx()
    rx.extend(abs(new_data))

threshold = 1500
output = []
start = 0
consecutive_count = 0
for i in range(len(rx)):
    if rx[i] > threshold:
        consecutive_count += 1

        if (consecutive_count == 1600):
            start = 1
            print('Start=',start, '  i =',i)

        if ((consecutive_count == 99)&(start==1)):
            output.append(1)
            consecutive_count = 0

        if ((consecutive_count == 900)&(start==1)):
            start = 0
            print('Start =',start, '  i =',i)


    else:
        consecutive_count = 0

print(" ")
print(len(output))
print(output)

plt.figure(figsize=[10,8])
plt.plot(rx)
plt.xlim(202800,202000+len(bit_array)*150)
# plt.figure(2)
# plt.plot(sample)
plt.show()