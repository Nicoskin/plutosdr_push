import numpy as np
import matplotlib.pyplot as plt
import adi
import time
import math
from scipy.fftpack import fft,fftshift


def sdr_settings(ip: str, frequency: int, buffer_size: int, sample_rate: int, tx_gain: int):  # Настройка sdr
    sdr = adi.Pluto(ip)

    #frequency = 2300e6+(2e6*2)
    sdr.rx_lo = int(frequency)
    sdr.tx_lo = int(frequency)

    sdr.rx_buffer_size = buffer_size
    sdr.sample_rate = sample_rate
    sdr.gain_control_mode_chan0 = 'manual'
    sdr.tx_hardwaregain_chan0 = tx_gain  # рекомендуемое значение от 0 до -50

    return sdr


sdr = sdr_settings("ip:192.168.2.1", 2300e6+(2e6*2), 1000, 1e6, -23)


t = np.linspace(0, 1, 1000)
fc = 10
i = np.cos(2 * np.pi * t * fc) * 2 ** 10
q = np.sin(2 * np.pi * t * fc) * 2 ** 10

samples = i + 1j * q

# # Генерируем QPSK-модулированный сигнал, 16 сэмплов на символ
# num_symbols = 1000
# x_int = np.random.randint(0, 4, num_symbols)  # 0 to 3
# #x_int = np.array(num_symbols)
# x_degrees = x_int*360/4.0 + 45  # 45, 135, 225, 315 град.
# x_radians = x_degrees*np.pi/180.0  # sin() и cos() в рад.
# # генерируем комплексные числа
# x_symbols = np.cos(x_radians) + 1j*np.sin(x_radians)
# samples = np.repeat(x_symbols, 16)  # 16 сэмплов на символ
# plt.figure(2)
# plt.plot(samples.real[:1000])
# plt.plot(samples.imag[:1000])
# samples *= 2**10  # Повысим значения для наших сэмплов

def create_bit_str(fio: str): # Функция преобразования строку в битовую последовательность | Возвращает bit_array
 
    encoded_bytes = fio.encode('ascii')
    # Преобразование байтов в массив битов
    bit_array = []
    for byte in encoded_bytes:
        bits = bin(byte)[2:].zfill(8)  # Преобразование в биты
        bit_array.extend([int(bit) for bit in bits])
   


    return bit_array

def binary_to_decimal(bit_array):
    decimal_list = []
    for i in range(0, len(bit_array), 2):
        # Получение двух битов и выполнение преобразования в десятичное число
        bits = bit_array[i:i+2]
        decimal_value = (bits[0] << 1) | bits[1]
        decimal_list.append(decimal_value)
    return decimal_list

bit_array = create_bit_str('raf')
x_int = binary_to_decimal(bit_array)
print(x_int)
x_degrees = []
for i in range(len(x_int)):
    x_degrees.append(x_int[i]*360/4.0 + 45)
x_degrees = np.array(x_degrees)
#x_degrees = x_int*360/4.0 + 45  # 45, 135, 225, 315 град.
x_radians = x_degrees*np.pi/180.0  # sin() и cos() в рад.
# генерируем комплексные числа
x_symbols = np.cos(x_radians) + 1j*np.sin(x_radians)
samples = np.repeat(x_symbols, 16)  # 16 сэмплов на символ
plt.figure(2)
plt.plot(samples.real[:1000])
plt.plot(samples.imag[:1000])
samples *= 2**10  # Повысим значения для наших сэмплов






sdr.tx_cyclic_buffer = True
sdr.tx(samples)
plt.figure(1)
for r in range(1):
    rx = sdr.rx()
    plt.clf()
    plt.plot(rx.real)
    # plt.plot(rx.imag)
    plt.ylim(-2000, 2000)
    plt.draw()
    plt.xlabel("Время")
    plt.pause(0.05)
    time.sleep(0.0001)

# plt.figure(2)
# tt = np.arange(-num_symbols/2,num_symbols/2)
# plt.plot(tt,abs(fftshift(fft(rx))))
# plt.xlabel('Частота')
# plt.ylabel('Амплитуда')
# plt.title('Спектр')

#plt.figure(4)
#plt.plot(samples.real[:1000])


plt.figure(3,figsize=(9, 9))
plt.scatter(np.real(rx), np.imag(rx), color='b',linewidths=0.002)
plt.scatter(np.real(samples), np.imag(samples), color='r')
plt.ylim(-2000, 2000)
plt.xlim(-2000, 2000)
plt.axhline(y = 0, color = 'r', linestyle = 'dashed')
plt.axvline(x = 0, color = 'r', linestyle = 'dashed')

# plt.plot(samples.real)
# plt.plot(samples.imag)
plt.show()
