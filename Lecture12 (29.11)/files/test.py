import numpy as np
import matplotlib.pyplot as plt
from mylib.sdr import *
import mylib as ml
import time 
sdr = sdr_settings("ip:192.168.2.1", 2000e6+(2e6*2)) # type: ignore

y = ml.str_to_bits('ice cream omg ice')
y = ml.str_to_bits('abcdefghijklmnopqrstuvwxyz')
sin = [+1, +1, +1, +1, +1, -1, -1, +1, +1, -1, +1, -1, +1]

sam = qam16(y)
sam_sin = bpsk(sin, 2**14)
sig = ml.merge_arr(sam_sin, sam)
sig = np.repeat(sig,10)

# plt.title('Сигнал на передачу')
# plt.scatter(sig.real,sig.imag)
# #plt.scatter(sam_sin.real,sam_sin.imag)
# plt.axhline(y = 0, color = 'r', linestyle = 'dashed')
# plt.axvline(x = 0, color = 'r', linestyle = 'dashed')
# plt.show()

tx_sig(sdr, sig)
#time.sleep(10)
rx = rx_cycles_buffer(sdr, 1)

#np.save("my_qpsk_bpsk_21_rx", rx)
#np.save("my_qam16_bpsk_11_all", rx)
rx = rx[::10]
rx = rx/np.max(rx.real)


rx = bpsk_sin(rx, sin)

rx = rx[len(sin):] * 3

def decode_qam16(rx_symbols):
    qam_symbols = {
        (0, 0, 0, 0): 1 + 1j,
        (0, 0, 0, 1): 1 + 3j,
        (0, 0, 1, 0): 3 + 1j,
        (0, 0, 1, 1): 3 + 3j,
        (0, 1, 0, 0): 1 - 1j,
        (0, 1, 0, 1): 1 - 3j,
        (0, 1, 1, 0): 3 - 1j,
        (0, 1, 1, 1): 3 - 3j,
        (1, 0, 0, 0): -1 + 1j,
        (1, 0, 0, 1): -1 + 3j,
        (1, 0, 1, 0): -3 + 1j,
        (1, 0, 1, 1): -3 + 3j,
        (1, 1, 0, 0): -1 - 1j,
        (1, 1, 0, 1): -1 - 3j,
        (1, 1, 1, 0): -3 - 1j,
        (1, 1, 1, 1): -3 - 3j,
    }
    
    decoded_bits = []
    
    for symbol in rx_symbols:
        min_distance = float('inf')
        closest_key = None
        for key, value in qam_symbols.items():
            distance = abs(symbol - value)
            if distance < min_distance:
                min_distance = distance
                closest_key = key
        decoded_bits.extend(closest_key)
    
    return decoded_bits


print(y)
e = decode_qam16(rx)
print(e)
print(ml.bits_to_str(e))


plt.figure(figsize=(7,7))
rx = np.array(rx)
# plt.plot(rx.real)
# plt.plot(rx.imag)
# plt.plot(abs(rx))
plt.scatter(rx.real,rx.imag)
plt.axhline(y = 0, color = 'r', linestyle = 'dashed')
plt.axvline(x = 0, color = 'r', linestyle = 'dashed')

plt.figure(2)
plt.plot(rx)
plt.plot(rx.imag)
plt.show()