import numpy as np
import matplotlib.pyplot as plt
import adi
import time

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

def create_bit_str(fio: str,start_bit:int, stop_bit:int): # Функция преобразования строку в битовую последовательность | Возвращает bit_array
    encoded_bytes = fio.encode('ascii')
    # Преобразование байтов в массив битов
    bit_array = []
    for byte in encoded_bytes:
        bits = bin(byte)[2:].zfill(8)  # Преобразование в биты
        bit_array.extend([int(bit) for bit in bits])

    bit_start = np.ones(start_bit) 
    bit_stop = np.ones(stop_bit)
    
    bit_array_list = list(bit_array)
    bit_array_list = list(bit_start) + bit_array_list + list(bit_stop) 
    bit_array = np.array(bit_array_list)

    return bit_array

def samples_from_bits(bit_array, symbol_length: int, amplitude_1: int, amplitude_0: int, add_samples_for_bits: int): # Функция преобразования samples в прямоугольный сигнал в зависимости от bit_array
    sample = np.zeros(len(bit_array)*(symbol_length+add_samples_for_bits), dtype=complex) # sample массив из длинны бит*symbol_length+add_samples_for_bits комплексных нулей 
    for i in range(len(bit_array)):
        for o in range(symbol_length):
            if bit_array[i] == 1:
                sample[i * symbol_length + o] = 1*amplitude_1 + 1j*amplitude_1
            elif bit_array[i] == 0:
                sample[i * symbol_length + o] = 1*amplitude_0 + 1j*amplitude_0
    
    return sample

def decoding_tx(rx, threshold: int, start_duration: int, stop_duration: int): # Функция декодирует сигнал rx находя 1 и 0
    output = []
    start = 0
    consecutive_count = 0
    count_zero = 0

    for i in range(len(rx)):
        if rx[i] > threshold:
            consecutive_count += 1

            if consecutive_count == start_duration:
                start = 1
                print('Start=', start, '  i =', i)  # debug
                consecutive_count = 0

            if (consecutive_count % 95 == 0) and (start == 1):
                output.append(1)
                #consecutive_count = 0

            if (consecutive_count == stop_duration) and (start == 1):
                start = 0
                delit = remove_ones_from_start(output)
                output = output[delit:-9]
                print('Start=', start, '  i =', i)  # debug

        elif (rx[i] < threshold):
            count_zero += 1
            if (count_zero % 80 == 0) and (start == 1):
                output.append(0)
            if consecutive_count != 0:
                count_zero = 0
            consecutive_count = 0
        else:
            consecutive_count = 0
            count_zero = 0
    
    return output

def rx_sig(samples, tx_cycle: bool): # Функция передает samples
    sdr.tx_cyclic_buffer = tx_cycle
    sdr.tx(samples)

def decoding_tx_debug(rx, threshold: int, start_duration: int, stop_duration: int, symbol_length: int, bit_adjustment: int): #Debug
    output = []
    start = 0
    consecutive_count = 0
    count_zero = 0
    x_values = []  # Добавлено для хранения значений x для графика
    colors = []    # Добавлено для хранения цветов для графика

    for i in range(len(rx)):
        if rx[i] > threshold:
            consecutive_count += 1

            if consecutive_count == start_duration:
                start = 1
                print('Start=', start, '  i =', i)  # debug
                consecutive_count = 0

            if (consecutive_count % symbol_length == 0) and (start == 1):
                output.append(1)
                x_values.append(i)
                colors.append('green')
                #consecutive_count = 0

            if (consecutive_count == stop_duration) and (start == 1):
                start = 0
                delit = remove_ones_from_start(output)
                x_values = x_values[delit:bit_adjustment]
                colors = colors[delit:bit_adjustment]
                output = output[delit:bit_adjustment]
                print('Start=', start, '  i =', i)  # debug

        elif (rx[i] < threshold):
            count_zero += 1
            if (count_zero % symbol_length == 0) and (start == 1):
                output.append(0)
                x_values.append(i)
                colors.append('red')
            if consecutive_count != 0:
                count_zero = 0
            consecutive_count = 0
        else:
            consecutive_count = 0
            count_zero = 0
    
    # Рисование графика
    plt.plot(rx)
    for x, color in zip(x_values, colors):
        plt.axvline(x=x, color=color, linestyle='--', linewidth=2)
    #plt.xlim(202800, 209000) # вывод начиная с самого сигнала
    plt.show()
    return output

def remove_ones_from_start(output):
    i = 0
    while i < len(output) and output[i] == 1:
        i += 1
    return i

def decrypt_binary_to_ascii(binary_list):
    #binary_list = int(binary_list)
    if len(binary_list) % 8 != 0:
        return "Длина массива должна быть кратной 8"
    
    # Разделим список на группы по 8 бит
    byte_strings = [binary_list[i:i+8] for i in range(0, len(binary_list), 8)]
    
    # Преобразуем каждую группу в десятичное число
    decimal_values = [int("".join(map(str, byte)), 2) for byte in byte_strings]
    
    # Преобразуем десятичные числа в символы ASCII и объединяем их
    decrypted_text = "".join([chr(decimal) for decimal in decimal_values])
    
    return decrypted_text

def decoding_rx(rx, threshold: int, start_duration: int, stop_duration: int, samples_for_bit:int, bit_adjustment: int):
    count_ones,count_zeros = 0,0
    output = []
    for i in range(len(rx)):
        if rx[i] > threshold: 
            count_ones += 1
            if count_ones == start_duration: 
                start = 1
                #print('Start=', start,' i =', i)  # debug
                count_ones = 0

            if count_ones % samples_for_bit == 0 and start == 1:
                output.append(1)

            if count_ones == stop_duration and start == 1:
                start = 0
                #print('Start=', start,' i =', i)  # debug
                count_ones = 0
                return output

            
        elif rx[i] < threshold and start == 1:
            count_ones = 0
            count_zeros += 1
            if count_zeros % samples_for_bit == 0 and start == 1:
                output.append(0)

        else:
            count_ones = 0
            count_zeros = 0

    return 0

def decoding_tx_debug2(threshold: int, start_duration: int, stop_duration: int, bit_adjustment: int): #Debug
    output = []
    start = 0
    consecutive_count = 0
    count_zero = 0
    x_values = []  # Добавлено для хранения значений x для графика
    colors = []    # Добавлено для хранения цветов для графика
    rx = sdr.rx()
    rx = abs(rx)
    for i in range(len(rx)):
        if rx[i] > threshold:
            consecutive_count += 1

            if consecutive_count == start_duration:
                start = 1
                print('Start=', start, '  i =', i)  # debug
                consecutive_count = 0

            if (consecutive_count % 18 == 0) and (start == 1):
                output.append(1)
                x_values.append(i)
                colors.append('green')
                #consecutive_count = 0

            if (consecutive_count == stop_duration) and (start == 1):
                start = 0
                delit = remove_ones_from_start(output)
                x_values = x_values[delit:bit_adjustment]
                colors = colors[delit:bit_adjustment]
                output = output[delit:bit_adjustment]
                print('Start=', start, '  i =', i)  # debug

        elif (rx[i] < threshold):
            count_zero += 1
            if (count_zero % 18 == 0) and (start == 1):
                output.append(0)
                x_values.append(i)
                colors.append('red')
            if consecutive_count != 0:
                count_zero = 0
            consecutive_count = 0
        else:
            consecutive_count = 0
            count_zero = 0
    
    # Рисование графика
    plt.plot(rx)
    for x, color in zip(x_values, colors):
        plt.axvline(x=x, color=color, linestyle='--', linewidth=2)
    #plt.xlim(202800, 209000) # вывод начиная с самого сигнала
    plt.show()
    return output

def rx_cycles_buffer(num_cycles: int):
    rx = []
    for i in range(num_cycles): # Считывает num_cycles циклов Rx
        new_data = sdr.rx()
        rx.extend(abs(new_data))
    return rx

"Настройка SDR"
#sdr = sdr_settings("ip:192.168.3.1", 2300e6+(2e6*2), 1000, 1e6,0,30) # type: ignore

"Кодирование слова | добавление start и stop"
bit_array = create_bit_str('rafe', 10, 5)

print('len bit_array =',len(bit_array[10:-5]))
for i in range(len(bit_array[10:-5])):
    if ((i) % 8) == 0 and (i!=0):
        print()
    print(int(bit_array[10+i]),end=' ')
print()

"Создание samples"
samples = samples_from_bits(bit_array, 20, 2**14, 2**1, 5) 

# plt.figure(1)
# plt.plot(samples)
# plt.show()

#output1 = decoding_tx_debug(samples, 7500, 200, 100, 18, -4)

# plt.plot(samples) # debug
# plt.show()

# for i in range(len(output1)):
#     if ((i) % 8) == 0 and (i!=0):
#         print()
#     print(int(output1[i]),end=' ')
# print()

"Передача samples циклически"
rx = rx_sig(samples, True)

# plt.figure(2)
# for r in range(30):
#     rx1 = sdr.rx()
#     plt.clf()
#     plt.plot(rx1.real)
#     # plt.plot(rx.imag)
#     plt.ylim(-2000, 2000)
#     plt.draw()
#     plt.xlabel("Время")
#     plt.pause(0.05)
#     time.sleep(0.01)

# plt.figure(1)
#plt.plot(rx)
#time.sleep(3)
#sdr.tx_destroy_buffer()

while True:
    "Приём Rx по 2000"
    rx = rx_cycles_buffer(2)
    #plt.plot(rx)
    output = decoding_rx(rx, 1000, 190, 90, 18, -5)
    if output != 0:
        break

#output = decoding_rx(1200, 195, 95, 16)
#output = decoding_tx_debug2(1200, 190, 90,-5)

# print(" ") # debug       
# print('len output =', len(output))
# print(output)       

print(" ")

print('Декодированное слово -', decrypt_binary_to_ascii(output))

#out_main_graph(rx) # Можно закоментить чтобы вывести что-то другое
         
# plt.figure(2)
# plt.plot(sample)
#time.sleep(3)

sdr.tx_destroy_buffer()
sdr.rx_destroy_buffer()
plt.show()