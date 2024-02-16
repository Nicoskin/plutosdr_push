import numpy as np
import matplotlib.pyplot as plt
import mylib as ml
import mylib.test as mltest

bit = ml.str_to_bits('ice cream abcdifghklmnopqrstuvwxyz')
sigPre = ml.qpsk(bit, 1)
sig = np.repeat(sigPre, 10)
noise = np.random.normal(0, 0.05, len(sig)) + 1j * np.random.normal(0, 0.05, len(sig))
sigTx = sig + noise

ml.cool_scatter(sigTx, show_plot=False)

sigRx = np.convolve(sigTx, np.ones(10)) / 10
#sigRx = sigRx[5:-5]
sigRx = sigRx[2:-8]

plt.figure(3)
plt.plot(sigTx, 'o-')
plt.plot(sigTx.imag, 'o-')
plt.figure(2)
plt.plot(sigRx, 'o-')
plt.plot(sigRx.imag, 'o-')

print(sigRx)
glaz = np.array(sigRx[:-9]).reshape(-1,10)
print(glaz)

plt.figure(4)
for p in glaz:
    plt.plot(p, 'o-')

plt.figure(5)
n = 20
for i in range(0, len(sigRx), n):
    plt.plot(sigRx[i:i+n], 'o-')




plt.show()