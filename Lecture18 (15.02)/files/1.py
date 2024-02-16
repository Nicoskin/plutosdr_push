import numpy as np
import matplotlib.pyplot as plt
import mylib as ml
import mylib.test as mltest

rx = np.load("D:/Documents/0__University/6semestr/test_python/test_npy_sdr/10_rx_2sdr.npy")

rx300 = rx[:300]

sv = np.convolve(rx300, np.ones(10))



plt.figure(1)
plt.plot(rx.real)
plt.plot(rx.imag)

plt.figure(2)
plt.plot(rx300.real)
plt.plot(rx300.imag)

plt.figure(3)
plt.plot(sv.real)
plt.plot(sv.imag)

ml.cool_scatter(rx300)
plt.show()