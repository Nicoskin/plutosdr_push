# Задание на практику ![](https://img.shields.io/badge/Done-green.svg)

# Задание
1. Реализация частотной синхронизации по циклическому принцыпу


# Выполнение
### Задание 1

```python
def freq_syn(self, ofdm, indexs):
    cp = self.CP_len  # Длина циклического префикса
    all_sym = self.N_fft + cp  # Общая длина символа (включая CP)

    for ind in indexs:
        # Нормализация первого и второго циклических префиксов (CP)
        fir = (ofdm[ind:ind + cp] / np.abs(ofdm[ind:ind + cp])).flatten()
        sec = (ofdm[ind + all_sym - cp:ind + all_sym] / np.abs(ofdm[ind + all_sym - cp:ind + all_sym])).flatten()

        # Расчет фазового сдвига с помощью нормированной кросс-корреляции
        eps = (1 / (2 * np.pi)) * np.sum(fir * sec.conj())  # Сопряженное для комплексной корреляции

        # Коррекция фазы для всех отсчетов в пределах символа
        for i in range(all_sym):
            ofdm[ind + i] *= np.exp(-1j * 2 * np.pi * eps * i / self.N_fft)

    return ofdm
```

По итогам тестирования приёма OFDM сигнала на SDR, эта частотная синхронизация не работает