import numpy as np
import matplotlib.pyplot as plt
import time

sig = np.repeat([1,2,1,2,1,1,1,2,2,1], 100)

#plt.plot(sig)
#plt.ylim(0.5,2.5)

numbers = [112, 117, 115, 104, 110, 105, 116, 115, 97] #pushnitsa
binary_string = ''.join(format(number, '08b') for number in numbers)


binary_variable = binary_string
binary_list = [int(bit) for bit in binary_string]
print(binary_list)
x=[]
symbol=12
for i in range(len(binary_list)):
    if(binary_list[i]==0):
        for p in range(symbol):
            x.append(1)
    else:
        for p in range(symbol):
            x.append(6)
x1=np.array(x)

plt.figure(2,figsize=[10,8])

plt.subplot(311)
plt.ylim(0.5,6.5)
plt.plot(x)

plt.subplot(312)
t=np.linspace(0,len(x1),len(x1))
print('len(t)=',len(t))
print('len(x1)=',len(x1))
fc=80
q=np.sin(2*np.pi*t*fc)
plt.plot(q)


plt.subplot(313)
sam = 2*(1.5*x1)*q
plt.plot(sam)



decoded_numbers = [int(binary_string[i:i+8], 2) for i in range(0, len(binary_string), 8)]
print(decoded_numbers)

decoded_string = ''.join(chr(number) for number in decoded_numbers)
print(decoded_string)


plt.show()