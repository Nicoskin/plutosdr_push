import numpy as np
import matplotlib.pyplot as plt
import mylib as ml
import mylib.test as mltest
import warnings
warnings.filterwarnings("ignore", category=np.ComplexWarning)

text_bit = ml.str_to_bits('ice cream asdhgasdhafdfsgdgsjfg')
#print(text_bit)
sig = np.repeat(text_bit, 10)
qpsk = ml.bpsk(sig, amplitude=2)
noise = np.random.normal(0, 0.1, len(qpsk))
qpsk = qpsk + noise
# plt.plot(qpsk)
print(len(qpsk))
ones = np.ones(10)
qpsk = np.convolve(qpsk,ones, mode='same')
print(len(qpsk))
# plt.plot(qpsk)
# plt.show()
#print(qpsk)
#np.reshape(qpsk,
#np.roll
rx = np.array(qpsk).reshape(-1,20) 
#rx = np.array(qpsk).reshape(3,-1) 
#rx = np.array(rx).reshape(-1,10) 
print(rx)
print(len(rx))
diag = rx[:, :5].flatten()
print('deag-->', diag)
#ml.cool_scatter(diag)


plt.figure(1)
#plt.plot(rx)
for symbol in rx:
    plt.plot(symbol)
plt.show()
