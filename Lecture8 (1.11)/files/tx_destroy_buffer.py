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


sdr = sdr_settings("ip:192.168.3.1", 2300e6+(2e6*2), 1000, 1e6,0,30) # type: ignore


sdr.tx_destroy_buffer()
sdr.rx_destroy_buffer()