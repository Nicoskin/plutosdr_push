import numpy as np
import matplotlib.pyplot as plt

v = 0.2 #частота
f = 0 #фаза
A = 1 #амплитуда

x = np.arange(0,100,0.1)
y = A*np.sin((x+f)*v)
z = A*np.cos((x+f)*v)

plt.plot(x,y)
plt.plot(x,z,'r')

plt.title("A * sin(w+f*t)")
plt.xlabel("время")
plt.ylabel("амплитуда")

plt.show()
