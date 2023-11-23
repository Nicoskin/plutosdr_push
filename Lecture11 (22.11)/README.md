# Задание на практику ![](https://img.shields.io/badge/Done-green.svg)

# Задание
1. Передать и получить АМ сигнал  
2. Передать и получить QPSK модулированный сигнал


# Выполнение
### Задание 1
Сырой сигнал RX

<img src="./photo/xrec1.png" width="600" /> 

```py
xrec = xrec1/np.mean(xrec1**2)
xrec_a = np.abs(np.real(xrec)) #вычисление модуля принимаемого сигнала
yf = np.convolve(xrec_a ,b)
np.abs(yf)
```
<img src="./photo/yf.png" width="600" /> 



### Задание 2
Использовал свою библиотеку для SDR (версии 0.0.6)

Первая попытка  
<img src="./photo/my_qpsk_rx1_plot.png" width="600" />
<img src="./photo/my_qpsk_rx1_scatter.png" width="357" />       

Изменил несущую частоту + разворот на нужный угол  
<img src="./photo/my_qpsk_rx2_plot.png" width="600" />
<img src="./photo/my_qpsk_rx2_scatter.png" width="357" />     

Без функции для разворота сигнала по синхронизации   
<img src="./photo/my_qpsk_rx3_plot.png" width="600" />
<img src="./photo/my_qpsk_rx3_scatter.png" width="357" />     


### Выполнено дома
Используя свой файл `my_qpsk_rx2.npy` с сырым полученным сигналом rx,    
я отбросил все лишние символы и оставил чистый сигнал

```py
symbol_length = 10
symbols = samples.reshape(-1, symbol_length)
extracted_symbols = symbols[:, 0]
```

<img src="./photo/home.png" width="700" /> 

На нижнем графике исходный массив который передавался(90 бит)   
На верхнем обработанный сигнал rx в котором остались одиночные символы(45 символов)
