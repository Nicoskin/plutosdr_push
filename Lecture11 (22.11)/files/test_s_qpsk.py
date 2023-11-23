import mylib as ml
from mylib.sdr import *
import numpy as np
import matplotlib.pyplot as plt

samples = np.load("my_qpsk_rx2.npy")

y = str_to_bits('ice cream', 20)
print(y)

# Разбиение на символы
symbol_length = 10
symbols = samples.reshape(-1, symbol_length)
extracted_symbols = symbols[:, 0]

# Применение функции к каждому символу и объединение результатов
def demodulate_qpsk_symbol(symbol):
    if np.real(symbol) > 0:
        if np.imag(symbol) > 0:
            return np.array([0, 0])
        else:
            return np.array([0, 1])
    else:
        if np.imag(symbol) > 0:
            return np.array([1, 0])
        else:
            return np.array([1, 1])

# Применение функции к каждому символу и объединение результатов в массив
decoded_bits_array = np.array([demodulate_qpsk_symbol(symbol) for symbol in extracted_symbols])
decoded_bits_array = decoded_bits_array.flatten()
print(decoded_bits_array)

# График смволов и пакета начальных бит
plt.subplot(211)
plt.plot(extracted_symbols.real)
#plt.plot(extracted_symbols.imag)
plt.subplot(212)
plt.plot(y)
plt.show()

# Отображение
plot1_scatter2 = 0 # 0-без доп графика 1-плот 2-скаттер

plt.figure(figsize=(9,7))
if plot1_scatter2 == 1:
    plt.plot(np.abs(samples))
    #plt.plot(samples.imag)
    plt.show()
    
elif plot1_scatter2 == 2:
    # plt.xlim(-0.03,0.03)
    # plt.ylim(-0.03,0.03)
    plt.scatter(extracted_symbols.real, extracted_symbols.imag)
    plt.axhline(y = 0, color = 'r', linestyle = 'dashed')
    plt.axvline(x = 0, color = 'r', linestyle = 'dashed')


    plt.show()