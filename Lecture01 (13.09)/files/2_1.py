import numpy as np
import random

t = []
for i in range(1024):
    n = random.randint(-1000,1000)
    t.append(n)
t.sort()

i=0
while i < len(t):
    if (t[i] <= 0):
        t.pop(i)
    else:
        i+=1

for i in range(len(t)):
    print(t[i], end=' ')

print('\n')
print("Len(t) =", len(t))