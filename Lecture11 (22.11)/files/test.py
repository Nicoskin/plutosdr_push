import numpy as np
import matplotlib.pyplot as plt
from mylib.sdr import *

# sdr = sdr_settings("ip:192.168.3.1", 2000e6+(2e6*2)) # type: ignore
# y = str_to_bits('ice cream', 20)
# sam = qpsk(y)
# sam = np.repeat(sam,10)
# tx_sig(sdr, sam)
# rx = rx_cycles_buffer(sdr, 1)
# rx = synchro_qpsk(rx, 10, 90)


#rx = rx/np.mean(rx**2)
#np.save("my_qpsk_rx", rx)

rx = np.load("my_qpsk_rx2.npy")


plt.figure(figsize=(7,7))
rx = np.array(rx)
# plt.plot(abs(rx))
plt.scatter(rx.real,rx.imag)
plt.axhline(y = 0, color = 'r', linestyle = 'dashed')
plt.axvline(x = 0, color = 'r', linestyle = 'dashed')

plt.figure(2, figsize=(12,7))
plt.plot(abs(rx))
# plt.plot(rx.real)
# plt.plot(rx.imag)

plt.show()