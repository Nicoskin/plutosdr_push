import numpy as np
import random

t = np.arange(1024)
for i in range(1024):
    t[i] = random.randint(-1000,1000)
t.sort()

x = np.arange(1024)

for i in range(1024):
    if (t[i] <= 0):
        x[i] = i
    else:
        x[i] = 0

x = np.delete(t,x)
for i in range(len(x)):
    print(x[i], end=' ')


print('\n')
print("Len(x) =", len(x))