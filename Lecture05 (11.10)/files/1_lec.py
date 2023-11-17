from scipy.fftpack import fft, ifft,  fftshift, ifftshift
from scipy import signal
from scipy.signal import kaiserord, lfilter, firwin, freqz
import numpy as np
import matplotlib.pyplot as plt

 
Ns = 2048 # количество дискретных отсчетов сигнала
Tmax = 10 # временной интервал формирования сигнала
dt=Tmax/(Ns-1)  # интервал дискретизации
fs = 1/dt #частота дисктеризации 
t=np.arange(0, 10,1/fs) 

Ac = 2   #амплитуда несущего колебания
fc = 4  #частота несущего колебания
wc = 2*np.pi*fc
xc = np.cos(wc*t) # Несущее колебание f=4

Am = 1.5 #амплитуда НЧ колебания
fm = 0.2  # Частота НЧ несущего колебания
wm = 2*np.pi*fm # модулирующий НЧ сигнал f=0.5
xm = np.cos(wm*t)

mu = Am/Ac #коэффициент модуляции
 
sam = Ac*(1+mu*xm)*xc # АМ сигнал 
plt.figure(1)
plt.subplot(311)
plt.plot(xm)
plt.subplot(312)
plt.plot(xc)
plt.subplot(313)
plt.plot(t,sam)
# plt.title('Колебание АМ ')
# plt.xlabel('t')
# plt.ylabel('$s_{AM}(t)$') 

# 1z
N=2048
plt.figure(10,figsize=[10,8])
plt.subplot(221)
plt.plot(t,xc)
plt.title('Несущее колебание')

plt.subplot(223)
X = fft(xc,N)/N
kf = np.arange(0, N)*fs/N
plt.stem(kf[0:100],abs(X[0:100]))
plt.title('Спектр несущего колебания')

plt.subplot(222)
plt.plot(t,xm)
plt.title('НЧ сигнал')

plt.subplot(224)
X = fft(xm,N)/N
kf = np.arange(0, N)*fs/N
plt.stem(kf[0:100],abs(X[0:100]))
plt.title('Спектр НЧ сигнала')

plt.show()

N=2048 # количество точек ДПФ
X = fft(sam,N)/N # вычисление ДПФ и нормирование на N
plt.figure(2)
kf = np.arange(0, N)*fs/N
plt.stem(kf[0:100],abs(X[0:100])) 
#plt.stem(X[0:100])
plt.title('Спектр АМ сигнала')
plt.xlabel('f')
plt.ylabel('$s_{AM}(f)$') 



s_d = sam**2 # квадратичный детектор, возводим принятое колебание в 2
plt.figure(3)
plt.plot(t,s_d)
plt.title('Колебание АМ при квадратичном детектировании')
plt.xlabel('t')
plt.ylabel('$s_{AM}(t)$') 


Xd = fft(s_d)/N # вычисление ДПФ и нормирование на N
plt.figure(4)
kf = np.arange(0, N)*fs/N
plt.stem(kf[0:100 ]   ,abs(Xd[0:100 ]  )) # спектр сигнала после возведения в 2
plt.title('Спектр колебания АМ при кв.дет. ')
plt.xlabel('f')
plt.ylabel('$s_{AM}(f)$') 

print(fs)


n=99
fn = fm/fs * 50
taps=signal.firwin(n,fn) # вычисляем ИХ ФНЧ с нормированной частотой 
d=2*signal.lfilter(taps,1.0,s_d) # сигнал на выходе ФНЧ (выход детектора)
plt.figure(5)
plt.plot(t,d)
plt.title('Сигнал на выходе ФНЧ детектора ')
plt.xlabel('t')
plt.ylabel('$m(t)$')

plt.figure(8) 
plt.stem(taps)
print(fn)

Xdd = fft(d)/N # вычисление ДПФ и нормирование на N
plt.figure(6)
kf = np.arange(0, N)*fs/N
plt.stem(kf[0:100]  ,abs(Xdd[0:100] )) 
plt.title('Спектр сигнала на выходе ФНЧ детектора ')
plt.xlabel('f')
plt.ylabel('$m(f)$') 

plt.show()