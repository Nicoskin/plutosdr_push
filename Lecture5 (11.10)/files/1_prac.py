import numpy as np
import matplotlib.pyplot as plt
import adi
import time

sdr = adi.Pluto("ip:192.168.2.1")

frequency = 2400e6+(2e6*2)
sdr.rx_lo = int(frequency)
sdr.tx_lo = int(frequency)

sdr.sample_rate = 1e6

fc = 10000
ts = 1/float(1e6)
t = np.arange(0, fc*ts, ts)
i = np.sin(2*np.pi*t*fc) * 2**14
q = np.cos(2*np.pi*t*fc) * 2**14
samples = i + 1j*q

# Start the transmitter
sdr.tx_cyclic_buffer = True # Enable cyclic buffers
sdr.tx(samples)


plt.figure(2)
for r in range(30):
    rx = sdr.rx()
    plt.clf()
    plt.plot(rx.real)
    #plt.plot(rx.imag)
    plt.ylim(-1000, 1000)
    plt.draw()
    plt.pause(0.05)
    time.sleep(0.0001)
    if(rx > 1000).any(): break
sdr.tx_destroy_buffer()
#plt.plot(x)
plt.show()