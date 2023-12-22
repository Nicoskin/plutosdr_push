import numpy as np
import adi
import matplotlib.pyplot as plt
import time

sample_rate = 1e5+9e5 # Hz
center_freq = 2e9 # Hz

sdr = adi.Pluto("ip:192.168.3.1")
sdr.sample_rate = int(sample_rate)
sdr.rx_lo = int(center_freq)
sdr.rx_buffer_size = 1000 


arr = []
for i in range(1,14):
    sample_rate = i*1e5 + 5e5
    print(sample_rate)
    sdr.sample_rate = int(sample_rate)

    start_time = time.time()
    for cycle in range(int(sample_rate/1e3)):
        rx = sdr.rx()
    end_time = time.time()

    print(end_time-start_time)
    arr.append(end_time-start_time)


plt.plot(np.arange(1,14)*1e5 + 5e5, arr)
plt.show()
#print(end_time-start_time)