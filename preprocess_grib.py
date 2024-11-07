# preprocess data
import pygrib
#from netCDF4 import Dataset

import netCDF4 as nc
from netCDF4 import Dataset
from osgeo import gdal, osr
import numpy as np

#1.2定义写图像文件的函数
def write_img(filename, im_proj, im_geotrans, im_data):
    # 判断栅格数据的数据类型
    print("判断栅格数据的数据类型")
    print(im_data.dtype.name)
    if 'int8' in im_data.dtype.name:
        datatype = gdal.GDT_Byte
    elif 'int16' in im_data.dtype.name:
        datatype = gdal.GDT_UInt16
    else:
        datatype = gdal.GDT_Float32
    # 判读数组维数
    print("判读数组维数")
    print(im_data.shape)   #(1440,)
    if len(im_data.shape) == 3:
        im_bands, im_height, im_width = im_data.shape
    else:
        im_bands, (im_height, im_width) = 1, im_data.shape     #问题在这 not enough values to unpack (expected 2, got 1)
    # 创建文件
    driver = gdal.GetDriverByName("GTiff")
    dataset = driver.Create(filename, im_width, im_height, im_bands, datatype)
    dataset.SetGeoTransform(im_geotrans)  # 写入仿射变换参数
    dataset.SetProjection(im_proj)  # 写入投影
    if im_bands == 1:
        dataset.GetRasterBand(1).WriteArray(im_data)  # 写入数组数据
    else:
        for i in range(im_bands):
            dataset.GetRasterBand(i + 1).WriteArray(im_data[i])
    del dataset

def nc_totif(input_path, output_path, time):
    # 读取nc文件
    tep_data = nc.Dataset(input_path)
    # 获取nc文件中对应变量的信息
    lon_data = tep_data.variables['lon'][:]
    lat_data = tep_data.variables['lat'][:]
    print(lon_data)
    print(lon_data.shape)
    # 影像的左上角&右下角坐标
    lonmin, latmax, lonmax, latmin = [lon_data.min(), lat_data.max(), lon_data.max(), lat_data.min()]
    # 分辨率计算
    num_lon = len(lon_data)  # 281
    num_lat = len(lat_data)  # 241
    lon_res = (lonmax - lonmin) / (float(num_lon) - 1)
    lat_res = (latmax - latmin) / (float(num_lat) - 1)
    # 分辨率
    print("分辨率：" + '\n')
    print("lon:" + str(lon_res))
    print("lat:" + str(lon_res))
    # 定义投影
    proj = osr.SpatialReference()
    proj.ImportFromEPSG(4326)  # WGS84
    proj = proj.ExportToWkt()  # 重点，转成wkt格式
    # print(prj)     字符串
    geotransform = (lonmin, lon_res, 0.0, latmax, 0.0, -lat_res)
    # 获取2m降水
    t2m = tep_data.variables['data'][:]  # (60, 241, 281)
    print('原始数据的维度')
    print(t2m.shape)   # (721, 1440)
    t2m_arr = np.asarray(t2m)
    print(tep_data.variables)
    outputpath = output_path + time + "_t2m.tif"
    write_img(outputpath, proj, geotransform, t2m_arr)

# first grib-->nc
# 打开GRIB文件
grib_file ='data/ddbb29908298e96942378da09989f604.grib'

grbs = pygrib.open(grib_file)
# 读取第一个GRIB将息,后续如果需要所有时间的数据需要加一个循环
temp = grbs.select()
print("总的grib数据大小：" + str(len(temp)))
grb = grbs.select()[0]
print("单个grib数据大小：")
print(grb.values)
print("===============")
print(grb.values.shape)
grbs.close()

# 创建NetCDF4文件
nc_file ='processed_data/output.nc'
nc_data = Dataset(nc_file,'w')
# 创建维度
latitudes = nc_data.createDimension('lat', len(grb.latitudes))
longitudes = nc_data.createDimension('lon', len(grb.longitudes))
lat_num = nc_data.createDimension('lat_num', grb.values.shape[0])
lon_num = nc_data.createDimension('lon_num', grb.values.shape[1])
print("创建维度===========")
print(grb.values.shape)  #(721, 1440)
print(latitudes)         #"<class 'netCDF4.Dimension'>": name = 'lat', size = 721
print(longitudes)        #"<class 'netCDF4.Dimension'>": name = 'lon', size = 1440
print(len(grb.latitudes))  #1038240
print(len(grb.longitudes))  #1038240
# 创建变量
latitude = nc_data.createVariable('lat','f4',('lat',))
longitude = nc_data.createVariable('lon','f4',('lon',))
data = nc_data.createVariable('data','f4',('lat_num', 'lon_num',))
print("创建变量===========")
print(latitude)
print(longitude)
print(data.shape)

# 设置变量的属性
latitude.units ='degrees north'
longitude.units = 'degrees east'
data.units = grb.units
#write to nc file
time = str(grb['dataDate']) + '_' + str(grb['stepRange'])
latitude[:]= grb.latitudes
longitude[:]= grb.longitudes
data[:,:]= grb.values
# close file
print(time)
grbs.close()
nc_data.close()

# nc文件输入输出路径
input_path = 'processed_data/output.nc'
output_path = "processed_data/"
# 读取nc文件，转换为tif文件
nc_totif(input_path, output_path, time)

