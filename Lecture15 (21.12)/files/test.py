import numpy as np
import matplotlib.pyplot as plt
import mylib as ml
from mylib.sdr import *

bit = ml.str_to_bits('ice cream')
bpsk_sig = bpsk(bit)
bpsk_sig = np.repeat(bpsk_sig, 10)

sdr = sdr_settings()
#sdr2 = sdr_settings("ip:192.168.2.1")
tx_sig(sdr, bpsk_sig)

rx = rx_cycles_buffer(sdr, 1) #

#plt.plot(rx)

plt.scatter(rx.real, rx.imag)
plt.axhline(y = 0, color = 'r', linestyle = 'dashed')
plt.axvline(x = 0, color = 'r', linestyle = 'dashed')
plt.show()