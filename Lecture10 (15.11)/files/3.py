import numpy as np
import matplotlib.pyplot as plt

c = np.load("1.csv.npy")

plt.plot(c)
plt.plot(c.imag)
plt.show()