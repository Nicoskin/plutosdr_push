import numpy as np
import matplotlib.pyplot as plt


n = 40
t = np.linspace(0, 1, n, endpoint=True)
x = np.sin(np.pi*t) + np.sin(2*np.pi*t) + np.sin(3*np.pi*t) + np.sin(5*np.pi*t)

plt.figure(figsize=(10,9))
plt.subplots_adjust(hspace=0.3,bottom=0.08,top=0.94)

plt.subplot(2, 2, 1)
plt.xlabel("Время")
plt.ylabel("Амплитуда")
plt.title("Аналоговый")
plt.grid()
plt.plot(t, x)

plt.subplot(2, 2, 2)
plt.xlabel("Время")
plt.ylabel("Амплитуда")
plt.title("Квантованный")
plt.grid()
plt.step(t, x)

plt.subplot(2, 2, 3)
plt.xlabel("Время")
plt.ylabel("Амплитуда")
plt.title("Дискретный")
plt.grid()
plt.stem(t, x)

plt.show()