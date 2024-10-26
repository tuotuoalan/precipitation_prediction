# -*- coding: utf-8 -*-
import netCDF4 as nc
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

def nc_totif(input_path, output_path):
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
    #date
    date = tep_data.variables['time']
    print(tep_data.variables)
    print(date)
    outputpath = output_path + str(date) + "_t2m.tif"
    write_img(outputpath, proj, geotransform, t2m_arr)
if __name__ == "__main__":
    # nc文件输入输出路径
    input_path = 'processed_data/output.nc'
    output_path = "processed_data/"
    # 读取nc文件，转换为tif文件
    nc_totif(input_path, output_path)
