# Задание на практику ![](https://img.shields.io/badge/Done-green.svg)

# Задание
1 Передать и получить АМ сигнал
2 Передать и получить QPSK модулированный сигнал


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
<img src="./photo/my_qpsk_rx1_scatter.png" width="400" /> 

Изменил несущую частоту + разворот на нужный угол
<img src="./photo/my_qpsk_rx2_plot.png" width="600" /> 
<img src="./photo/my_qpsk_rx2_scatter.png" width="400" /> 

Без функции для разворота сигнала по синхронизации 
<img src="./photo/my_qpsk_rx3_plot.png" width="600" /> 
<img src="./photo/my_qpsk_rx3_scatter.png" width="400" /> 
