import numpy as np
import matplotlib.pyplot as plt
import mylib as ml
import mylib.test as mlt
from icecream import ic

bits = ml.str_to_bits("A small text to send to the radio channel")  # 328 бита
sigQpsk = ml.qpsk(bits, 1)  # 164 символа

sample_rate = int(1e6)  # 1 млн
N_subcarriers = 16  # 32 Поднесущих
symbol_length = 16 # Длительность символа равна количеству поднесущих 
guardInterval = 4

sigQpsk = np.concatenate((sigQpsk, [0+0j] * (N_subcarriers - (len(sigQpsk) % N_subcarriers)))) # добавление в конце нулей
# y = np.concatenate((sigQpsk[0 * N_subcarriers//2 : 1 * N_subcarriers//2],[0+0j],sigQpsk[1 * N_subcarriers//2 : 2 * N_subcarriers//2]))
# ic(sigQpsk[0 * N_subcarriers//2 : 1 * N_subcarriers//2])
# ic(sigQpsk[1 * N_subcarriers//2 : 2 * N_subcarriers//2])
# ic(sigQpsk[0 * N_subcarriers : 1 * N_subcarriers])
# ic(y)
arr_symbols = np.array(())
for i in range(int(len(sigQpsk) / N_subcarriers)):  # 5
    y = np.concatenate((sigQpsk[i * N_subcarriers//2 : (i+1) * N_subcarriers//2],[0+0j],sigQpsk[(i+1) * N_subcarriers//2 : (i+2) * N_subcarriers//2]))
    sym = np.fft.ifft(sigQpsk[i * N_subcarriers : (i + 1) * N_subcarriers], symbol_length)
    arr_symbols = np.concatenate((arr_symbols, sym[-guardInterval:],sym))

arr_symbols = arr_symbols / np.max(arr_symbols.real) # Нормализация

# #cor = np.correlate(arr_symbols, arr)
# ic(cor)
# plt.figure(10)
# plt.plot(cor)

# Шум
noice = 0.02
arr_symbols = arr_symbols + np.random.normal(0, noice, len(arr_symbols)) + 1j * np.random.normal(0, noice, len(arr_symbols)) 
#arr_symbols = arr_symbols[5:-995] # смещение на 1 символ

arr_symbols_Rx = np.array(())
for i in range(int(len(arr_symbols) / symbol_length)):  # 5
    sym = np.fft.fft(arr_symbols[i * symbol_length : (i + 1) * symbol_length])
    sym = sym[:N_subcarriers]
    arr_symbols_Rx = np.concatenate((arr_symbols_Rx, sym))

arr_symbols_Rx = arr_symbols_Rx / np.max(arr_symbols_Rx.real) # Нормализация

dem = ml.dem_qpsk(arr_symbols_Rx)
decoded = ml.bits_to_str(dem)
ic(decoded)

ml.cool_plot(arr_symbols)
ml.cool_plot(arr_symbols_Rx)
ml.cool_plot(sigQpsk)
ml.cool_scatter(arr_symbols_Rx)

plt.show()
