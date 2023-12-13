import numpy as np
import matplotlib.pyplot as plt
from mylib.sdr import *
import mylib as ml

sdr = sdr_settings("ip:192.168.2.1", 2000e6+(2e6*2), rx_gain=20) # type: ignore

y = ml.str_to_bits('ice cream')
sin = [+1, +1, +1, +1, +1, -1, -1, +1, +1, -1, +1, -1, +1]

sam = qpsk(y)
#sam_sin = bpsk(sin, 2**14)
#sig = ml.merge_arr(sam_sin, sam)
#sig = np.repeat(sig,10)
sig = np.repeat(sam,10)

# plt.scatter(sig.real, sig.imag)
# plt.show()

tx_sig(sdr, sig)
rx = rx_cycles_buffer(sdr,2)
rx = rx/np.max(rx.real)
np.save("10_rx_2sdr(3)", rx)
plt.scatter(rx.real, rx.imag)


rx_4 = rx ** 4 
fur = np.fft.fft(rx_4)
fur = np.fft.fftshift(fur)
argmax = np.argmax(fur)
print(argmax)
w = np.linspace(-np.pi,np.pi,len(rx))
#print(w[argmax])
fi = w[argmax] / 4
print(fi)
#rx = rx * np.exp(-1j * fi)

# Параметры
iter = 2000  # Число попыток найти Δφ
exp_fine = np.zeros(iter)  # Массив длиной в iter итераций
exp_fine[0] = 1
fi_e = np.zeros(iter)
a1 = 0.1  # Коэффициент фильтра
kc = 0.03  # Коэффициент интегратора
integrator_out = 0
fi_n = 0  # Первоначальная оценка сдвига фазы

for n in range(iter):
    exp_fine[n] = np.exp(1j * fi_n)
    fi_e[n] = np.angle(rx * exp_fine[n]) * a1
    integrator_out += fi_e[n] * kc
    fi_n += integrator_out  # Обновление оценки фазы с учетом выхода интегратора
    

print(fi_e)
plt.figure(5)
plt.plot(fi_e)
plt.figure(1)
fi = fi_e[-1:]
print(fi)

rx = rx * np.exp(-1j * fi)


plt.scatter(rx.real, rx.imag)
#plt.scatter(corrected_rx.real, corrected_rx.imag)
plt.axhline(y = 0, color = 'r', linestyle = 'dashed')
plt.axvline(x = 0, color = 'r', linestyle = 'dashed')
plt.show()
plt.plot(np.arange((-len(fur)/2),(len(fur)/2)),abs(fur))
#plt.show()

#np.save("my_qam16_bpsk_11_all", rx)
rx = rx[::10]
rx = rx/np.max(rx.real)
