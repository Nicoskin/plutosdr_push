import numpy as np
import matplotlib.pyplot as plt
import adi
import time
import math
from scipy.fftpack import fft


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
#sdr = sdr_settings("ip:192.168.2.1", 2000e6, 1000, 1e6, 0)

t = np.linspace(0, 1, 1000)
fc = 10
i = np.cos(2 * np.pi * t * fc) * 2 ** 10
q = np.sin(2 * np.pi * t * fc) * 2 ** 10

samples = i + 1j * q

# Генерируем QPSK-модулированный сигнал, 16 сэмплов на символ
num_symbols = 1000
x_int = np.random.randint(0, 4, num_symbols)  # 0 to 3
x_degrees = x_int*360/4.0 + 45  # 45, 135, 225, 315 град.
x_radians = x_degrees*np.pi/180  # sin() и cos() в рад.
# генерируем комплексные числа
x_symbols = np.cos(x_radians) + 1j*np.sin(x_radians)
samples = np.repeat(x_symbols, 16)  # 16 сэмплов на символ
samples *= 2**10  # Повысим значения для наших сэмплов


#p = np.sqrt(i**2 + q**2)
# plt.plot(p)
sdr.tx_cyclic_buffer = True
sdr.tx(samples)

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
# plt.plot(abs(fft(rx)))
# plt.xlabel('Частота')
# plt.ylabel('Амплитуда')
# plt.title('Спектр')

# plt.plot(samples.real)
# plt.plot(samples.imag)
plt.show()
