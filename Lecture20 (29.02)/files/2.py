import numpy as np
import matplotlib.pyplot as plt
import mylib as ml
import mylib.test as mlt
from icecream import ic

bits = ml.str_to_bits("A small text to send to the radio channel")  # 328 бита
sigQpsk = ml.qpsk(bits, 1)  # 164 символа


sample_rate = int(1e6)  # 1 млн

N_subcarriers = 10  # 32 Поднесущих
symbol_length = 100 # Длительность символа равна количеству поднесущих 

sigQpsk = np.concatenate((sigQpsk, [0+0j] * (N_subcarriers - (len(sigQpsk) % N_subcarriers)))) # добавление в конце нулей

arr_symbols = np.array(())
for i in range(int(len(sigQpsk) / N_subcarriers)):  # 5
    sym = np.fft.ifft(sigQpsk[i * N_subcarriers : (i + 1) * N_subcarriers], symbol_length)
    arr_symbols = np.concatenate((arr_symbols, sym))

plt.figure(10)
for i in range(N_subcarriers): 
    sym1 = np.fft.ifft(sigQpsk[i:i+1], symbol_length)
    shift_amount = 1 + i/symbol_length
    shifted_sym1 = sym1 * np.exp(1j*2*np.pi*shift_amount*np.arange(symbol_length))
    fft = np.fft.fftshift(np.fft.fft(shifted_sym1, int(1e6)))
    plt.plot(abs(fft))

arr_symbols = arr_symbols / np.max(arr_symbols.real) # Нормализация

ml.cool_plot(np.fft.fftshift(abs(np.fft.fft(arr_symbols[:64], int(1e6)))))

#ic(len(arr_symbols))
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
