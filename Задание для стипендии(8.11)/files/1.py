import numpy as np
import matplotlib.pyplot as plt
import adi
import time
import random
import cmath
from scipy.fft import fft,fftshift

def sdr_settings(ip:str, frequency: int, buffer_size: int, sample_rate: int, tx_gain: int, rx_gain: int): # Настройка sdr
    sdr = adi.Pluto(ip)

    sdr.rx_lo = int(frequency)
    sdr.tx_lo = int(frequency)

    sdr.rx_buffer_size = buffer_size
    sdr.sample_rate = sample_rate
    sdr.gain_control_mode_chan0 = 'manual'
    sdr.tx_hardwaregain_chan0 = tx_gain # рекомендуемое значение от 0 до -50
    sdr.rx_hardwaregain_chan0 = rx_gain # рекомендуемое значение от 0 до -50

    return sdr

sdr = sdr_settings("ip:192.168.3.1", 900e6, 1000, 1e6,0,15) # type: ignore

def tx_sig(samples, tx_cycle: bool): # Функция передает samples
    sdr.tx_cyclic_buffer = tx_cycle
    sdr.tx(samples)

def rx_cycles_buffer(num_cycles: int):
    rx = []
    for i in range(num_cycles): # Считывает num_cycles циклов Rx
        new_data = sdr.rx()
        rx.extend((new_data))
    return rx

# Переменные для задания
N = 50
Fs = 500000
Ns = 25

random_bits = [random.choice([0, 1]) for _ in range(N)] #создание рандомных битов

random_bits = [1] * 20 + random_bits # добавление 20 единиц в начале
#random_bits = random_bits[:-50]
# Создание QPSK-символов из бит
qpsk_symbols = []
for i in range(0, len(random_bits), 2):
    I = 2 * random_bits[i] - 1  # In-phase компонента
    Q = 2 * random_bits[i + 1] - 1  # Quadrature компонента
    symbol = I + 1j * Q
    symbol = np.tile(symbol, Ns)  # Повторение символа Ns раз для длительности символа
    qpsk_symbols.extend(symbol)
qpsk_symbols *= 2**13


#print(random_bits)
bit_pairs = [random_bits[i:i+2] for i in range(0, len(random_bits), 2)] # Разделите битовую последовательность на пары битов
decimal_numbers = [int(''.join(map(str, pair)), 2) for pair in bit_pairs] # Преобразуйте каждую пару битов в десятичное число
#print(decimal_numbers)

#Генерируем QPSK-модулированный сигнал, 16 сэмплов на символ
num_symbols = 1000
decimal_numbers = np.array(decimal_numbers)
#x_degrees = decimal_numbers*360/4.0 #+ 95 # +компенсация шумов по фазе
#x_radians = x_degrees*np.pi/180.0 # sin() и cos() в рад.
x_degrees = 45 + (90 * decimal_numbers)
x_radians = (45 + (90 * decimal_numbers)) * np.pi / 180.0
x_symbols = np.cos(x_radians) + 1j*np.sin(x_radians) #генерируем комплексные числа
samples = np.repeat(x_symbols, Ns) # 16 сэмплов на символ
samples *= 2**14 #Повысим значения для наших сэмплов

plt.figure(figsize=(8,6))
plt.plot(samples)
plt.title("Samples")
plt.xlabel("Samples")
plt.ylabel("Амплитуда")
plt.show()
#plt.stem(fftshift(fft(samples)))

psd = np.abs(np.fft.fftshift(np.fft.fft(samples)))**2
psd_dB = 10*np.log10(psd)
f = np.linspace(len(samples)/-2, len(samples)/2, len(psd))
plt.plot(f/1e6, psd_dB)
plt.title("{} сэмплов на символ".format(Ns))
#plt.xlabel("Частота")
# plt.plot(samples.imag)
# plt.show()
# plt.plot(qpsk_symbols)
plt.show()

tx_sig(samples, True)
rx = rx_cycles_buffer(3)
sdr.tx_destroy_buffer()
sdr.rx_destroy_buffer()
plt.plot(rx)
#plt.show()
k=0
threshold = 50
target_angle = -2.12
ygol = 0
for i in range(len(rx)):
    if abs(rx[i] - rx[i-1]) < threshold:
        k += 1
    else:
        k=0
    if k == 490:
        print(i, rx[i])
        # current_angle = cmath.phase(rx[i])
        # angle_difference = target_angle - current_angle
    
        # # Модифицируем комплексное число, чтобы установить его угол равным целевому углу
        # ygol = current_angle + angle_difference
        # rx[i] = cmath.rect(abs(rx[i]), ygol)

        # # Выводим измененное комплексное число и его угол
        # print('Измененное rx[{}]: {}, Угол: {:.2f}'.format(i, rx[i], cmath.phase(rx[i])))

        # angle = cmath.phase(rx[i])
        # #if angle < 0: angle += 3
        # print(angle)
        # rx[i] = complex(rx[i].real * -0.522, rx[i].imag * -0.85)

        # print('изм',rx[i])
        # angle = cmath.phase(rx[i])
        # print(angle)

# for i in range(len(rx)):
#     current_angle = cmath.phase(rx[i])
#     angle_difference = target_angle - current_angle

#     # Модифицируем комплексное число, чтобы установить его угол равным целевому углу
#     ygol = current_angle + angle_difference
#     rx[i] = cmath.rect(abs(rx[i]), ygol)

plt.figure(3,figsize=(9, 9))
plt.scatter(np.real(rx), np.imag(rx), color='b',linewidths=0.002)
#plt.scatter(np.real(samples), np.imag(samples), color='r')
plt.ylim(-2000, 2000)
plt.xlim(-2000, 2000)
plt.axhline(y = 0, color = 'r', linestyle = 'dashed')
plt.axvline(x = 0, color = 'r', linestyle = 'dashed')

plt.show()

psd = np.abs(np.fft.fftshift(np.fft.fft(rx)))**2
psd_dB = 10*np.log10(psd)
f = np.linspace(len(rx)/-2, len(rx)/2, len(psd))
plt.plot(f/1e6, psd_dB)
plt.title("80 сэмплов на символ")
plt.xlabel("Частота [MHz]")
plt.ylabel("PSD")
#plt.show()
