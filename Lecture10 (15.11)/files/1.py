import matplotlib.pyplot as plt
import numpy as np

x = np.array([+1, +1, +1, -1, -1, -1, +1, -1, -1, +1, -1]) # код Баркера из 11
#x = np.array([+1, +1, +1, -1, +1]) # код Баркера из 5
y = np.correlate(x,x,'full') # подсчёт корреляции


plt.plot(y)
plt.ylabel("Корреляция")
plt.xlabel("Сдвиг")

plt.show()