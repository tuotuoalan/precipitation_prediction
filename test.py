import xarray as xr
'''
CMIP5_trdata = "processed_data/CMIP5_daily_precipitation_data/pr_day_CESM1-CAM5_historical_r1i1p1_20050101-20051231.nc"
temp = xr.open_dataset(CMIP5_trdata)
print(temp['pr'])
print(temp['pr'].values)
temp.close()

print("分割线==========================================")
CMIP5_trdata = "processed_data/pr_day_CESM1-CAM5_historical_r1i1p1_20050101-20051231.nc"
temp = xr.open_dataset(CMIP5_trdata)
print(temp['pr'])
print(temp['pr'].values)
temp.close()
'''

print("分割线==========================================")
CMIP5_trdata = "ERA5_2000to2004_orig_daily_precipitation.nc"
temp = xr.open_dataset(CMIP5_trdata)
print(temp['tp'])
#print(temp['tp'].values)
temp.close()

print("分割线==========================================")
CMIP5_trdata = "pr_day_bcc-csm1-1_historical_r1i1p1_20000101-20041231.nc"
temp = xr.open_dataset(CMIP5_trdata)
print(temp['pr'])
temp.close()


