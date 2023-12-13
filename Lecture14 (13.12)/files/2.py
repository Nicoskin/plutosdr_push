import numpy as np
import matplotlib.pyplot as plt
import mylib as ml
from mylib.sdr import *

bit = ml.str_to_bits('ice cream')
qpsk_sig = qpsk(bit)
qpsk_sig = np.repeat(qpsk_sig, 10)

sdr1 = sdr_settings("ip:192.168.2.1", frequency=2e9 + 7e6)
sdr2 = sdr_settings("ip:192.168.3.1", frequency=2e9 + 7e6)
tx_sig(sdr1, qpsk_sig)

rx2 = rx_cycles_buffer(sdr2,1)
rx1 = rx_cycles_buffer(sdr1,1)

####
iter=len(rx2)
phi1 = np.zeros(iter) # фаза на выходе петли PLL для коррекции сигнала
s_loop =  np.zeros(iter, dtype = complex)
dds_mult =  np.zeros(iter, dtype = complex)
phi_error =  np.zeros(iter)
phi_error_filtered =  np.zeros(iter)

phi1[0]=1

int_out = 0
Kp = 0.001 # коэффициент пропорциональности 
Ki = 0.001 # коэффициент интегратора 

# for i in range(len(rx1)):
#     rx2[i] = rx2[i] * np.exp(-1j * (i*0.1))

# for i in range(iter-1):
#     s_loop[i]=np.exp(1j*phi1[i])
#     dds_mult[i]=rx2[i]*np.conjugate(s_loop[i])
#     #dds_mult[i]=xrec[i]*np.conjugate(s_loop[i])# 
#     phi_error[i]=np.imag(dds_mult[i]) # фазовая ошибка 
#     #phi_error[i]=np.imag(xrec[i])*np.real(s_loop[i])-np.real(xrec[i])*np.imag(s_loop[i])
#     #phi_error[i]=np.angle(dds_mult[i])
#     prop_out = phi_error[i]*Kp
#     int_out = phi_error[i]*Ki+int_out
#     phi_error_filtered[i]=prop_out+int_out
#     phi1[i+1]=phi1[i]+phi_error_filtered[i]

# xrecc=rx2*s_loop
###

# plt.figure(3)
# plt.scatter(xrecc.real,xrecc.imag)

np.save("rx2",rx2)

plt.figure(2, figsize=(9,9))
plt.subplot(221)
plt.scatter(rx1.real,rx1.imag)
plt.axhline(0,color='r')
plt.axvline(0,color='r')
plt.subplot(222)
plt.scatter(rx2.real,rx2.imag)
#plt.plot(rx2.real[:30],rx2.imag[:30])
plt.axhline(0,color='r')
plt.axvline(0,color='r')
# plt.subplot(224)
# for i in range(len(rx1)):
#     rx2[i] = rx2[i] * np.exp(1j * (i*0.049))
# plt.scatter(rx2.real[:30],rx2.imag[:30])
# plt.plot(rx2.real[:30],rx2.imag[:30])
# plt.axhline(0,color='r')
# plt.axvline(0,color='r')
# plt.subplot(224)
# plt.scatter(xrecc.real,xrecc.imag)

# plt.figure(1)
# plt.plot(rx2.real)
# plt.plot(rx2.imag)
# plt.scatter(rx1.real,rx1.imag)
# plt.axhline(0,color='r')
# plt.axvline(0,color='r')
sdr1.tx_destroy_buffer()
plt.show()