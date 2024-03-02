import numpy as np
import matplotlib.pyplot as plt
import mylib as ml
import mylib.test as mlt
from icecream import ic

T = 1e-4  # Длительность символа
Nc = 16  # Количество поднесущих
df = 1/T  # Частотный интервал между поднесущими
ts = T/Nc  # Интервал дискретизации

k = 1
t = ts * np.arange(0, Nc)
s = 1/np.sqrt(T)*np.exp(1j*2*np.pi*k * df*t)  # Формирование одной поднесущей с частотой f ∗ d f
ml.cool_plot(s.real)
sc_matr = np.zeros((Nc, len(t)), dtype=complex)
sd = np.zeros((1, Nc), dtype=complex)
# Матрица из поднесуших
for k in range(Nc):
    sk_k = 1/np.sqrt(T) *np.exp(1j*2*np.pi*k* df * t)
    sc_matr[k,:] = sk_k

#sd − вектор Nc передаваемых комплексных символов
sd=np.sign(np.random.rand(1,Nc)-0.5)+1j*np.sign(np.random.rand(1,Nc)-0.5)
sd=sd.reshape(Nc)
xt=np.zeros((1,len(t)),dtype=complex)

# формирование суммы модулированных поднесущих
for k in range(Nc):
    sc=sc_matr[k,:]
    xt=xt+sd[k]*sc

xt=xt.reshape(Nc)
# реальная часть сформированного OFDM символа
ml.cool_plot(xt.real)
plt.figure(1)
plt.plot(sc_matr)

plt.show()