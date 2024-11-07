import pygrib
import matplotlib.pyplot as plt
import numpy as np
import netCDF4 as nc
from netCDF4 import Dataset
import xarray as xr
plt.rcParams['font.sans-serif']=['SimHei'] #显示中文标签
plt.rcParams['axes.unicode_minus']=False   #这两行需要手动设置

# 打开GRIB文件
def Grib_info(grib_file):
    grbs = pygrib.open(grib_file)
    # 读歌第一个GRIB将息
    grb = grbs.select()[0]
    grb1 = grbs.select()[1]
    print(grb)
    print(grb1)
    print(grb.keys())
    print("================lats, lons")
    lats, lons = grb.latlons()
    print(lats)
    print(len(lats))
    print(lons)
    print(len(lats))
    print("================shortName")
    print(grb.shortName)
    print("================")
    array = grb.values
    print(array)
    grbs.close()

def NC_info(filepath):
    nf = nc.Dataset(filepath, 'r')
    print(nf.variables.keys())
    print("=============================")
    print(nf.variables)
    nf.close()

#处理数据，将降水数据得单位m/hour转换为mm/day
def ERA5_process_total_precipitation(file_path):  #这是原本采用的数据单位为m的时候的转换
    nc_trdata = Dataset(file_path, 'r+')
    # 数据*1000 ————>mm/day
    print("before values:==============================")
    print(nc_trdata.variables.keys())
    new_data = nc_trdata['tp']
    print(new_data[:, :, :])
    nc_trdata['tp'][:, :, :] = np.multiply(new_data, 1000)
    nc_trdata.close()
    print("after value===================================")
    temp = xr.open_dataset(file_path)
    print(temp['tp'].values)
    temp.close()

#处理数据，将降水数据得单位kg m-2 s-1转换为mm/day
def Data_Process_Unit_Conversion_CMIP5(file_path):
    nc_trdata = Dataset(file_path, 'r+')
    # 数据*24*3600 ————>mm/day
    print("before values:==============================")
    print(nc_trdata.variables.keys())
    new_data = nc_trdata['pr']
    print(new_data[:, :, :])
    nc_trdata['pr'][:, :, :] = np.multiply(new_data, 24 * 3600)
    nc_trdata.close()

def Data_Process_Unit_Conversion_ERA5(file_path):
    nc_trdata = Dataset(file_path, 'r+')
    # 数据*1000 ————>mm/day
    print("before values:==============================")
    print(nc_trdata.variables.keys())
    new_data = nc_trdata['mcpr']
    print(new_data[:, :, :])
    nc_trdata['mcpr'][:, :, :] = np.multiply(new_data, 24 * 3600)
    nc_trdata.close()
    print("after value===================================")
    temp = xr.open_dataset(file_path)
    print(temp['mcpr'].values)
    temp.close()


if __name__ == '__main__':
    grib_file = 'data/ddbb29908298e96942378da09989f604.grib'
    CMIP5_trdata = "pr_day_bcc-csm1-1_historical_r1i1p1_20000101-20041231.nc"
    CMIP5_tedata = "pr_day_bcc-csm1-1_historical_r1i1p1_20050101-20051231.nc"
    ERA5_orig_trdata = "ERA5_2000to2004_orig_daily_precipitation.nc"
    ERA5_orig_tedata = "2005_total_precipitation_4506344e7b521f176066569eaa796e1e.nc"

    # deal with ERA5 data
    #ERA5_process_total_precipitation(ERA5_orig_trdata)
    ERA5_process_total_precipitation(ERA5_orig_tedata)
    #Data_Process_Unit_Conversion_ERA5(ERA5_orig_trdata)
    #Data_Process_Unit_Conversion_ERA5(ERA5_orig_tedata)

    # deal with CMIP5 data
    #Data_Process_Unit_Conversion_CMIP5(CMIP5_trdata)
    #Data_Process_Unit_Conversion_CMIP5(CMIP5_tedata)








