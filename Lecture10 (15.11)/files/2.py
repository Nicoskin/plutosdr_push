import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.signal import max_len_seq
import adi

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


data = max_len_seq(5)[0]

m = 2*data-1

ft = 100e3
fs = 600e3
ns = fs/ft

b = np.ones(int(ns))  # Коэффициенты фильтра интерполятора

ts1 =np.array([0,0,1,0,0,1])
ts1 = 2*ts1-1
x_IQ = np.hstack((ts1,m)) # формирование пакета
#print(len(x_IQ))

N_input = len(x_IQ)
xup = np.hstack((x_IQ.reshape(N_input, 1), np.zeros((N_input, int(ns-1)))))


xup = xup.flatten()
#print(xup)
x1 = signal.lfilter(b, 1, xup)
x = x1.astype(complex)   # type: ignore
print(x)
xt = .5*(1+x)  # комплексные отсчеты для adalm
triq = 2**14*xt
print(len(triq))
#print(triq)
n_frame= len(triq)
#sdr.tx(triq)
print(triq)

plt.plot(triq)
plt.show()
# sdr = sdr_settings("ip:192.168.3.1", 1000e6, 1000, 1e6,0,15) # type: ignore
# sdr.rx_rf_bandwidth = 200000
# sdr.rx_destroy_buffer()
# sdr.tx_hardwaregain_chan0 = -10
# sdr.rx_buffer_size = 2*n_frame
# sdr.tx_cyclic_buffer = False
# sdr.tx(triq)
# xrec1=sdr.rx()
# xrec = xrec1/np.mean(xrec1**2)
# np.save('1.csv', xrec)
