import numpy as np

V_bs = 7500 # [м/c]
V_ue = 2500 # [м/c]

F_dl = 15e9 # [Hz]
F_ul = 10e9 # [Hz]

coord_bs = np.array([0, 0, 5e5]) #[м] xyz
coord_ue = np.array([0, 0, 1e4]) #[м] xyz

dis_bu = np.array(coord_bs - coord_ue)
print('dis_bu',dis_bu)

V_ue_rx = V_ue*dis_bu[2] / (np.sum(dis_bu**2) ** 0.5)
V_bs_rx = V_bs*dis_bu[2] / (np.sum(dis_bu**2) ** 0.5)
print('V_ue_rx',V_ue_rx)
print('V_bs_rx',V_bs_rx)

F_dl_ue = F_dl * (1+(V_ue_rx + V_bs_rx) / 3e8)
F_ul_ue = F_ul * (1-(V_ue_rx + V_bs_rx) / 3e8)
print(f'F_dl_ue = {F_dl_ue:_}') # [Hz]
print(f'F_ul_ue = {F_ul_ue:_}') # [Hz]
