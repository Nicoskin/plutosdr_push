from scipy.fftpack import fft, ifft,  fftshift, ifftshift
import numpy as np
import matplotlib.pyplot as plt

t=np.arange(0,0.9,0.01)
x=np.cos(2*np.pi*t*2)

#plt.figure(1)
plt.subplot(2,1,1)
plt.title("cos 2Hz")
plt.plot(t,x)

X=np.array([0,1,0,0,0,0,0,0])
t=np.arange(0,8)
N=20

print(len(t))

x_ifft = fft(X,N)
t = np.arange(0, len(x_ifft))/N

#plt.figure(2)
plt.subplot(2,1,2)
plt.title("1 на 2/8")
plt.plot(t ,np.real(x_ifft))
plt.subplots_adjust(hspace=0.4)
#plt.plot(t,x)
plt.show()
