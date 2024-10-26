import pygrib

# first grib-->nc
# 打开GRIB文件
grib_file ='data/ddbb29908298e96942378da09989f604.grib'

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
'''
import xarray as xr
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import cartopy.io.shapereader as shpreader
import matplotlib.ticker as mticker
import matplotlib.pyplot as plt
#import cmaps
#数据读取及处理
ds=xr.open_dataset("data/ddbb29908298e96942378da09989f604.grib",engine='cfgrib')
print("grib数据的key：")
print(ds.keys())
tp=ds['TP_GDS0_SFC_acc1h']*1000 #单位转换为mm
tp.attrs['units']='mm'
#画图
proj=ccrs.PlateCarree()  #创建投影
fig=plt.figure(figsize=(12,8))
ax=fig.subplots(1,1,subplot_kw={'projection':proj})

#中国经纬度范围
region = [70,140,15,55]
ax.set_extent(region,crs=proj)
# 设置地图属性:加载国界、海岸线、河流、湖泊
#ax.add_feature(cfeat.BORDERS.with_scale('50m'), linewidth=0.8, zorder=1)
ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.6, zorder=1)
#ax.add_feature(cfeature.RIVERS.with_scale('50m'), zorder=1)
ax.add_feature(cfeature.LAKES.with_scale('50m'), zorder=1)

# 设置网格点属性
gl = ax.gridlines(ylocs=np.arange(region[2],region[3]+10,10),xlocs=np.arange(region[0],region[1]+10,10),draw_labels=True,linestyle='--',alpha=0.7)
gl.xlabels_top = False
gl.ylabels_right = False
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER

##标题
ax.set_title('Total Precipitation',loc='left',fontsize =12)
ax.set_title('Time:2020071300(UTC)',loc='right',fontsize =12)
# 设置colorbar
cbar_kwargs = {
   'orientation': 'horizontal',
   'label': 'Total Precipitation (mm)',
   'shrink': 0.8,
   'ticks': np.arange(0,20+5,5)
}
#要素绘制
levels=np.arange(0,20+0.5,0.5)
tp.plot.contourf(ax=ax, levels=levels, cmap='pink_r', cbar_kwargs=cbar_kwargs, transform=ccrs.PlateCarree())

#shp文件
china = shpreader.Reader('/home/kesci/work/assignment_1/China_basic_map/bou2_4l.dbf').geometries()

##绘制中国国界省界九段线等等
ax.add_geometries(china, proj,facecolor='none', edgecolor='black',zorder = 1)
##添加南海
sub_ax = fig.add_axes([0.705, 0.351, 0.15, 0.15],projection = proj)
sub_ax.set_extent([105, 125, 0, 25], crs=ccrs.PlateCarree())
sub_ax.add_feature(cfeature.COASTLINE.with_scale('50m'))
china = shpreader.Reader('/home/kesci/work/assignment_1/China_basic_map/bou2_4l.dbf').geometries()
sub_ax.add_geometries(china, ccrs.PlateCarree(),facecolor='none', edgecolor='black',zorder = 1)

'''
