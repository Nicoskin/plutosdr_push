import numpy as np
import matplotlib.pyplot as plt
import mylib as ml
import mylib.test as mlt
from icecream import ic 

#########
### Создание данных
#########
bits = ml.str_to_bits('A small text to send to the radio channel') # 328 бита
sigQpsk = ml.qpsk(bits, 1) # 164 символа

sample_rate = int(1e6) # 1 млн
symbol_length = int(sample_rate / 1e4) # 100 сэмплов на символ

freq_ofdm = 10 # Гц
N_subcarriers = 1

t = np.arange(0, symbol_length)
arr = []
for i in range(0, N_subcarriers):
    delta_freq = freq_ofdm + 1*(i/symbol_length) # K = 1
    ic(delta_freq)
    xt = sigQpsk[i] * np.exp(1j*np.pi*2 * delta_freq * t)
    arr.append(xt)

arr_sum = np.sum(arr, axis=0)

arr_ifft = np.fft.ifft(sigQpsk[:N_subcarriers], 100) # Создание OFDM 

arr_fft = np.fft.fft(arr_ifft)

ic(arr_fft[:N_subcarriers])

decod = []
for i in range(1, N_subcarriers):
    delta_freq = freq_ofdm + 1*(i/symbol_length) # K = 1
    decod.append(arr_fft[i] * np.exp(1j*np.pi*2 * t * delta_freq))
#ic(decod)

x = np.exp(1j*np.pi*2 * t * 10.01)
y = x * arr_sum

uu = x * arr_ifft
k1 = np.sum(uu)

ic(sigQpsk[:N_subcarriers])
#ic(k1)

plt.figure(9)
plt.plot(decod)

plt.figure(7)
plt.plot(arr_ifft)

plt.figure(8)
plt.plot(arr_fft)

plt.figure(3)
plt.plot(arr_sum)
#plt.plot(y)

plt.figure(4)
plt.plot(abs(np.fft.fftshift(np.fft.fft(arr_sum, int(1e6)))) / 100)
#plt.plot(abs(np.fft.fftshift(np.fft.fft(uu, int(1e6)))))
plt.plot(abs(np.fft.fftshift((arr_fft))))
plt.grid()

plt.figure(1)
for p in arr:
    plt.plot(p)
    
plt.figure(2)
plt.plot(sigQpsk[:32])
plt.plot(sigQpsk[:32].imag)
#plt.plot(arr)


plt.show()