import matplotlib 
matplotlib.use("Agg")
from define_parameters import *
import glob
from netCDF4 import Dataset
import matplotlib.pyplot as plt

from define_parameters import pspc_data_folder,years, plots_folder, initial_final_day_index_EOBS, name
from define_parameters import output_path as files_path
import numpy as np

ini_year=str(np.array(years).astype('int').min())
end_year=str(np.array(years).astype('int').max())


files_folder='/store/c2sm/pr04/jvergara/SATELLITE/CMSAF/'


cmsaf_data_path='/store/c2sm/pr04/jvergara/SATELLITE/CMSAF/season_means/'
sample_cmsaf_file=np.load(cmsaf_data_path+'CMSAF_SW_2002_DJF.npy')

units='W/m2'
levels_lw=np.linspace(120,300,15).tolist()
levels_lw_diff=np.linspace(-50,50,16).tolist()
levels_sw=np.linspace(0,400,20).tolist()
levels_sw_diff=np.linspace(-50,50,16).tolist()
#levels_sw_diff=[-50,-45,-40,-35,-30,-25,-20,-15,-10,-5,5,10,15,20,25,30,35,40,50]
#levels_lw_diff=[-50,-45,-40,-35,-30,-25,-20,-15,-10,-5,5,10,15,20,25,30,35,40,50]
n_years=len(years)
arrays_shape=(4,n_years,sample_cmsaf_file.shape[0],sample_cmsaf_file.shape[1])


arrays_shape=(4,n_years,sample_cmsaf_file.shape[0],sample_cmsaf_file.shape[1])
cmsaf_lw=np.zeros(arrays_shape)
model_lw=np.zeros(arrays_shape)


cmsaf_sw=np.zeros(arrays_shape)
model_sw=np.zeros(arrays_shape)



for iseason in range(4):
    season=jle.seasons[iseason]
    print(season)
    for iyear in range(n_years):
        year=years[iyear]
        print(year)
        ds=Dataset(files_path+'lffd'+year+'_'+season+'_regrided_CMSAF.nc')
        model_data=-ds.variables['ATHB_T'][0,]
        cmsaf_data=np.load(cmsaf_data_path+'CMSAF_LW_'+year+'_'+season+'.npy')
#        eobs_data_mask=np.load(cmsaf_data_path+'EOBS_temp_mask_'+year+'_'+season+'.npy')
        cmsaf_lw[iseason,iyear,:,:]=cmsaf_data
        model_lw[iseason,iyear,:,:]=model_data
        
        
        
        ds=Dataset(files_path+'lffd'+year+'_'+season+'_regrided_CMSAF.nc')
        model_data=ds.variables['ASOB_T'][0,]
        cmsaf_data=np.load(cmsaf_data_path+'CMSAF_SW_'+year+'_'+season+'.npy')
#        eobs_data_mask=np.load(cmsaf_data_path+'EOBS_temp_mask_'+year+'_'+season+'.npy')
        cmsaf_sw[iseason,iyear,:,:]=cmsaf_data
        model_sw[iseason,iyear,:,:]=model_data

X,Y=np.meshgrid(ds.variables['lon'][:],ds.variables['lat'][:])




sample_nc=Dataset(run_path+'1h/lffd20060613120000.nc')
lat_bounds=[sample_nc.variables['lat'][:].min(),sample_nc.variables['lat'][:].max()]
lon_bounds=[sample_nc.variables['lon'][:].min(),sample_nc.variables['lon'][:].max()]


bias_sw=model_sw-cmsaf_sw
mask=(model_sw<0)
bias_sw[mask]=np.nan
bias_sw_annual_mean=np.nanmean(bias_sw,axis=1)
#%%
plt.figure(figsize=(18,14))
for iseason in range(4):
    season=jle.seasons[iseason]
    print(season)
    iplot=iseason+1
    plt.subplot(2,2,iplot)
    plt.title(season)


    jle.Quick_plot(bias_sw_annual_mean[iseason] ,'SW TOA '+ini_year+'-'+end_year+' '+season+' MB %1.1f '%(np.nanmean(bias_sw_annual_mean[iseason]))+units,
                   levels=levels_sw_diff,latitudes=Y,longitudes=X,
                   cmap=plt.cm.RdBu_r,extend=1,new_fig=0,cb_format='%1.2f',cb_label=units,lat_bounds=lat_bounds,lon_bounds=lon_bounds,projection='rot_pol')

plt.savefig(plots_folder+'Seasonal_SW_biases_'+name+'.png')

#%%

bias_lw=model_lw-cmsaf_lw
mask=(model_lw>100000)
bias_lw[mask]=np.nan
bias_lw_annual_mean=np.nanmean(bias_lw,axis=1)

#%%

plt.figure(figsize=(18,14))
for iseason in range(4):
    season=jle.seasons[iseason]
    print(season)
    iplot=iseason+1
    plt.subplot(2,2,iplot)
    plt.title(season)

    jle.Quick_plot(bias_lw_annual_mean[iseason] ,'LW TOA '+ini_year+'-'+end_year+' '+season+' MB %1.1f '%(np.nanmean(bias_lw_annual_mean[iseason]))+units,
                   levels=levels_lw_diff,latitudes=Y,longitudes=X,
                   cmap=plt.cm.RdBu_r,extend=1,new_fig=0,cb_format='%1.2f',cb_label=units,lat_bounds=lat_bounds,lon_bounds=lon_bounds,projection='rot_pol')
plt.savefig(plots_folder+'Seasonal_LW_biases_'+name+'.png')

