import numpy as np
import matplotlib.pyplot as plt
import mylib as ml
import mylib.test as mltest
import warnings

warnings.filterwarnings("ignore", category=np.ComplexWarning)

text_bit = ml.str_to_bits("ice cream ahsjdadjhqgdjhhasjkdhwuyecuih")
sig = np.repeat(text_bit, 10)
bpsk = ml.bpsk(sig, amplitude=2)
noise = np.random.normal(0, 0.1, len(bpsk))
noise = noise + 1j * np.random.normal(0, 0.1, len(bpsk))
bpsk = bpsk + noise
# for i in range(len(bpsk)):
#     bpsk[i] = bpsk[i] * np.exp(1j * 0.002*i)
# ml.cool_scatter(bpsk)
# print(len(bpsk))
# print(bpsk)
ones = np.ones(10)
bpsk = np.convolve(bpsk, ones, mode="same")
plt.plot(bpsk.real)
plt.plot(bpsk.imag)

plt.figure(2)
t, o = 10, []
for i in range(0, len(bpsk) - t, t):
    print(i)
    rx = bpsk[i : i + t]
    o.append(bpsk[i + 5])
    print(rx)
    plt.plot(rx)

plt.show()
o = np.array(o)
ml.cool_scatter(o)
print(o)
