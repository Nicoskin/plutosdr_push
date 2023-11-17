import numpy as np
import matplotlib.pyplot as plt
import time 
from random import randint

x=np.arange(10,5000000,200000)
y=[]
z=[]

for i in range(10,5000000,200000):
    list = [i]
    for j in range(i):
        list.append(randint(-100,100))

    start = time.time() 
    list.sort()
    end = time.time() - start 

    y.append(end)

    print(i)
    list1 = np.random.sample(i)
        
    start1 = time.time() 
    np.sort(list1)
    end1 = time.time() - start1 
    
    z.append(end1)



plt.plot(x,y,'r')
plt.plot(x,z,'g')
plt.ylabel("Время")
plt.xlabel("Кол-во элементов")
plt.show()
