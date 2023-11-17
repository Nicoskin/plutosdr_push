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

def create_bit_str(fio: str): # Функция преобразования строку в битовую последовательность | Возвращает bit_array
    encoded_bytes = fio.encode('ascii')
    # Преобразование байтов в массив битов
    bit_array = []
    for byte in encoded_bytes:
        bits = bin(byte)[2:].zfill(8)  # Преобразование в биты
        bit_array.extend([int(bit) for bit in bits])

    bit_start = np.ones(20) # 20 бит, тк в начале не всё передаётся
    bit_stop = np.ones(10)
    
    # debug
    #print('len(bit_array) =',len(bit_array)))

    # for i in range(len(bit_array)):
    #     print(int(bit_array[i]), end=' ')
    #     if (i + 1) % 8 == 0:
    #         print()

    bit_array_list = list(bit_array)
    bit_array_list = list(bit_start) + bit_array_list + list(bit_stop) # Добавление стартовых 16 бит и конечных 10
    bit_array = np.array(bit_array_list)

    # debug
    #print('len(start+bit_array+stop) =', len(bit_array))

    # for i in range(len(bit_array)):
    #     print(int(bit_array[i]), end=' ')
    #     if (i + 1) % 8 == 0:
    #         print()

    return bit_array

def samples_from_bits(bit_array, symbol_length: int, amplitude_1: int, amplitude_0: int): # Функция преобразования samples в прямоугольный сигнал в зависимости от bit_array
    sample = np.zeros(len(bit_array)*(symbol_length+10), dtype=complex) # sample массив из длинны бит*110 комплексных нулей (не 100 чтобы потом немного пустого места было)
    for i in range(len(bit_array)):
        for o in range(symbol_length):
            if bit_array[i] == 1:
                sample[i * symbol_length + o] = 1*amplitude_1 + 1j*amplitude_1
            elif bit_array[i] == 0:
                sample[i * symbol_length + o] = 1*amplitude_0 + 1j*amplitude_0
    
    return sample

def decoding_tx(rx, threshold: int, start_duration: int, stop_duratio: int): # Функция декодирует сигнал rx находя 1 и 0
    output = []
    start = 0
    consecutive_count = 0
    for i in range(len(rx)):
        if rx[i] > threshold:
            consecutive_count += 1

            if (consecutive_count == start_duration):
                start = 1
                print('Start=',start, '  i =',i) # debug

            if ((consecutive_count == 99) and (start==1)):
                output.append(1)
                consecutive_count = 0

            if ((consecutive_count == stop_duratio) and (start==1)):
                start = 0
                print('Start =',start, '  i =',i) # debug

        else:
            consecutive_count = 0

    return output

def rx_sig(samples, tx_cycle: bool, start_tx: int): # Функция передает samples начиная с ±(start_tx * 1000 + 3000) семпла | Возвращает массив rx
    sdr.tx_cyclic_buffer = tx_cycle
    rx = []
    for i in range(1000): # Считывает секунду Rx
        if (i==start_tx): # На start_tx * 1000 семпле начать Tx
            sdr.tx(samples)

        new_data = sdr.rx()
        rx.extend(abs(new_data))

    return rx

def out_main_graph(rx): # Функция выводит rx
    plt.figure(1, figsize=[10,8])
    plt.title("Сигнал")
    plt.xlabel("samples") 
    plt.ylabel("amplitude")
    plt.xlim(202800, 203500+len(samples)) # вывод начиная с самого сигнала
    plt.plot(rx)

def decoding_tx_debug(rx, threshold: int, start_duration: int, stop_duration: int): #Debug
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

            if (consecutive_count % 95 == 0) and (start == 1):
                output.append(1)
                x_values.append(i)
                colors.append('green')
                #consecutive_count = 0

            if (consecutive_count == stop_duration) and (start == 1):
                start = 0
                x_values = x_values[:-10]
                colors = colors[:-10]
                output = output[:-10]
                print('Start=', start, '  i =', i)  # debug

        elif (rx[i] < threshold):
            count_zero += 1
            if (count_zero % 80 == 0) and (start == 1):
                output.append(0)
                x_values.append(i)
                colors.append('red')
            if consecutive_count != 0:
                count_zero = 0
            consecutive_count = 0
        else:
            consecutive_count = 0
            count_zero = 0
    
    delit = remove_ones_from_start(output)
    output = output[i:]  # Удаление единиц в начале

    # Рисование графика
    plt.plot(rx)
    for x, color in zip(x_values, colors):
        plt.axvline(x=x, color=color, linestyle='--', linewidth=2)

    plt.show()
    return output

def remove_ones_from_start(output):
    i = 0
    while i < len(output) and output[i] == 1:
        i += 1
    return i

#sdr = sdr_settings("ip:192.168.2.1", 2300e6+(2e6*2), 1000, 1e6,0,0)

bit_array = create_bit_str('raf')

samples = samples_from_bits(bit_array, 100, 2**14, 2**1) 

output1 = decoding_tx_debug(samples, 7500, 1600, 1000)
# plt.plot(samples) # debug
# plt.show()
print(output1)

#rx = rx_sig(samples, False, 200)

output = decoding_tx(rx, 1500, 1600, 900)

# print(" ") # debug       
# print(len(output))
# print(output)       

out_main_graph(rx) # Можно закоментить чтобы вывести что-то другое
         
# plt.figure(2)
# plt.plot(sample)

plt.show()