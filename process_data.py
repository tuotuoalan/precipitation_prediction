import glob
import xarray
import netCDF4 as nc
import xarray as xr

#合并多个nc文件，因为ERA5下载的日降水只能一年一年下载
def Merge_multiple_NCfiles(path, outputpath):
    all_files = glob.glob(path + '*.nc')
    all_files.sort()
    print(all_files[0])
    data = nc.Dataset(all_files[0])
    print(data.variables)

    file_new = []
    for i in range(len(all_files)):
        file = xarray.open_dataset(all_files[i])['tp']
        file_new.append(file)
        print('第' + str(i) + '个文件的数据个数是：' + str(len(file)))
        print('===================================================')
    da = xarray.concat(file_new, dim='valid_time')
    da.to_netcdf(outputpath)

    # 打印处理后的数据
    with xarray.open_dataset(outputpath) as f:
        tp = f.tp
    print(tp)


#截取CMIP5中2000年1月1日之后的数据，确保和训练时的ERA5数据时间一致
def Extract_specific_time_of_NCfiles(path):
    nc_data = xr.open_dataset(path)
    f = nc_data.assign_coords(time=nc_data.indexes['time'].to_datetimeindex())
    v = f['pr']  # pr为变量内容（降雨）
    print(v[1])

    nc_train = v.loc['2000-1-1':'2004-12-31']  # 截取时间
    nc_test = v.loc['2005-1-1':'2005-12-31']  # 截取时间
    nctr_coordinate = nc_train.loc[:, :, :]  # 截取经纬度
    ncte_coordinate = nc_test.loc[:, :, :]  # 截取经纬度

    ds1 = xr.Dataset({'pr': nctr_coordinate})
    ds2 = xr.Dataset({'pr': ncte_coordinate})
    ds1.to_netcdf('processed_data/pr_day_bcc-csm1-1_historical_r1i1p1_20000101-20041231.nc')
    ds2.to_netcdf('processed_data/pr_day_bcc-csm1-1_historical_r1i1p1_20050101-20051231.nc')
    print('success')

if __name__ == '__main__':
    #merge multiple ERA5 nc files
    #inputpath = 'processed_data/era5_orig_daily_precipitation/'
    #outputpath = "processed_data/ERA5_2000to2004_orig_daily_precipitation.nc"
    #Merge_multiple_NCfiles(inputpath, outputpath)

    path = 'processed_data/pr_day_bcc-csm1-1_historical_r1i1p1_18500101-20121230.nc'
    Extract_specific_time_of_NCfiles(path)