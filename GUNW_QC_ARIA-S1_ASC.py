import glob
import os
import netCDF4 as nc
import matplotlib.pyplot as plt
import numpy as np


# 取得第一個 nc 檔案
nc_files = sorted(glob.glob("./data_gunw/ASC/*.nc"))
if not nc_files:
    raise FileNotFoundError("./data_gunw/ASC 目錄內找不到 .nc 檔案！")

nc_file = nc_files[0]
print(f"正讀取檔案：{os.path.basename(nc_file)}")

with nc.Dataset(nc_file, 'r') as ds:
    # 進入 ARIA 指定網格群組
    grid_grp = ds.groups['science'].groups['grids'].groups['data']
    
    # 讀取相干性陣列
    coherence = grid_grp.variables['coherence'][:]
    
    # 自動匹配經緯度 / 座標欄位名稱
    vars_list = grid_grp.variables
    if 'longitude' in vars_list:
        x_coords = vars_list['longitude'][:]
        y_coords = vars_list['latitude'][:]
    elif 'xCoordinates' in vars_list:
        x_coords = vars_list['xCoordinates'][:]
        y_coords = vars_list['yCoordinates'][:]
    elif 'x' in vars_list:
        x_coords = vars_list['x'][:]
        y_coords = vars_list['y'][:]
    else:
        raise KeyError(f"未匹配到座標變數，群組內現有變數為：{list(vars_list.keys())}")

# 設定繪圖邊界 [x_min, x_max, y_min, y_max]
extent = [x_coords.min(), x_coords.max(), y_coords.min(), y_coords.max()]

plt.figure(figsize=(9, 7))
im = plt.imshow(coherence, extent=extent, cmap='gray', origin='upper')
plt.colorbar(im, label='Coherence')

# 自動辨識投影或經緯度標籤
if x_coords.max() > 180:
    plt.xlabel('Easting (m)')
    plt.ylabel('Northing (m)')
    plt.title('Mailiao InSAR Coherence (UTM Coordinates)')
else:
    plt.xlabel('Longitude (°E)')
    plt.ylabel('Latitude (°N)')
    plt.title('Mailiao InSAR Coherence (WGS84)')

plt.grid(True, linestyle='--', alpha=0.5)
plt.savefig('qc_mailiao_ARIA-S1_asc.png', dpi=300)
plt.show()
