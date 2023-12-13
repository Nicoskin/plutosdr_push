import numpy as np
import matplotlib.pyplot as plt
import mylib as ml
from mylib.sdr import * 

str = ml.str_to_bits('asdefg')
tx_signal = qpsk(str)
print(tx_signal)

sdr = sdr_settings('ip:192.168.3.1')
tx_sig(sdr, tx_signal)
rx = rx_cycles_buffer(sdr, 3)

