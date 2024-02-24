import numpy as np
import matplotlib.pyplot as plt
import mylib as ml
import mylib.test as mlt
from icecream import ic

bits = ml.str_to_bits("A small text to send to the radio channel")  # 328 бита
sigQpsk = ml.qpsk(bits, 1)  # 164 символа


sample_rate = int(1e6)  # 1 млн
symbol_length = int(sample_rate / 1e4)  # 100 сэмплов на символ

freq_ofdm = 10  # Гц
N_subcarriers = 32  # 32 Поднесущих

#ic((len(sigQpsk) % N_subcarriers))
sigQpsk = np.concatenate((sigQpsk, [0+0j] * (N_subcarriers - (len(sigQpsk) % N_subcarriers)))) # добавление в конце нулей
#ic(len(sigQpsk))
arr_symbols = np.array(())
for i in range(int(len(sigQpsk) / N_subcarriers)):  # 5
    sym = np.fft.ifft(sigQpsk[i * N_subcarriers : (i + 1) * N_subcarriers], symbol_length)
    arr_symbols = np.concatenate((arr_symbols, sym))

arr_symbols = arr_symbols / np.max(arr_symbols.real) # Нормализация

#ic(len(arr_symbols))
# Шум
noice = 0.05
arr_symbols = arr_symbols + np.random.normal(0, noice, len(arr_symbols)) + 1j * np.random.normal(0, noice, len(arr_symbols)) 
#arr_symbols = arr_symbols[5:-995] # смещение на 1 символ

arr_symbols_Rx = np.array(())
for i in range(int(len(arr_symbols) / symbol_length)):  # 5
    sym = np.fft.fft(arr_symbols[i * symbol_length : (i + 1) * symbol_length])
    sym = sym[:32]
    arr_symbols_Rx = np.concatenate((arr_symbols_Rx, sym))

arr_symbols_Rx = arr_symbols_Rx / np.max(arr_symbols_Rx.real) # Нормализация
#ic(len(arr_symbols_Rx)) 

#ic(arr_symbols_Rx[-32:])
dem = ml.dem_qpsk(arr_symbols_Rx)
#ic(dem)
decoded = ml.bits_to_str(dem)
# decoded = decoded.rstrip('\x00')
ic(decoded)

plt.figure(1)
plt.plot(arr_symbols)
plt.plot(arr_symbols.imag)

plt.figure(2)
plt.plot(arr_symbols_Rx)
plt.plot(arr_symbols_Rx.imag)

plt.figure(3)
plt.plot(sigQpsk)
plt.plot(sigQpsk.imag)

ml.cool_scatter(arr_symbols_Rx)

plt.show()
