import numpy as np
import matplotlib.pyplot as plt
import adi
import time

# Заданные параметры
f = 8
fs = 256
a = 1

# Создание временной оси
t = np.arange(0, 1, 1/fs)
# Генерация входного сигнала
x = a * np.cos(2*np.pi * f * t )
x2 = a * np.cos(2*np.pi * f*2 * t )
x = x + x2

norm_f = 0.3*np.pi
analog_f = norm_f*(fs/(2*np.pi))
print(analog_f)

X = np.fft.fft(x) # Вычисление ДПФ сигнала


# Создание импульсной характеристики ФНЧ
fc = 8/fs  # Нормированная частота среза
N = 51 # Длина импульсной характеристики
n = np.arange(0, N) 
h = np.sinc(2 * fc * (n - (N - 1) / 2))  # Импульсная характеристика ФНЧ
filtered_signal = np.convolve(x, h, mode='same')/3

plt.figure(figsize=(10, 6))
plt.plot(t, x, label='Входной сигнал')
plt.title('Входной сигнал и отфильтрованная fs*2 частота')
plt.xlabel('Время')
plt.plot(t, filtered_signal, label='Отфильтрованный сигнал')
plt.grid()
plt.legend()
plt.tight_layout()
plt.show()

XX = np.fft.fft(filtered_signal) # Вычисление ДПФ сигнала
freq_axis = np.fft.fftfreq(len(XX), 1/fs)

# Вычисление частотной оси в Герцах
freq_axis = np.fft.fftfreq(len(XX), 1/fs)
plt.figure(1,figsize=[8,6])
plt.subplot(211)
plt.stem(freq_axis, np.abs(XX))
plt.xlabel("Частота (Гц)")
plt.ylabel("Модуль спектра")
plt.title("Спектр отфильтрованного сигнала")
plt.xlim(-30,30)
plt.grid()

plt.subplot(212)
plt.stem(freq_axis, np.abs(X))
plt.xlabel("Частота (Гц)")
plt.ylabel("Модуль спектра")
#plt.title("Спектр сигнала при Fs = {}".format(fs))
plt.title("Спектр сигнала")
plt.xlim(-30,30)
plt.grid()
plt.show()

# plt.figure(2,figsize=[8,6])
# plt.plot(t,x)
# plt.xlabel("Время")
# plt.ylabel("Амплитуда")
# plt.title("cos({} * t) + cos({} * t) fs = {}".format(f,f*2,fs))
# #plt.title("cos() {}Гц fs = {}".format(f,fs))
# plt.show()