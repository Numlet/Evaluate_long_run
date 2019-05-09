#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  9 14:44:22 2019

@author: jvergara
"""

import matplotlib 
matplotlib.use("Agg")
from define_parameters import *
import glob
from netCDF4 import Dataset
import matplotlib.pyplot as plt

from define_parameters import pspc_data_folder,years, plots_folder, initial_final_day_index_EOBS, name
from define_parameters import output_path as files_path


ini_year=str(np.array(years).astype('int').min())
end_year=str(np.array(years).astype('int').max())

temp_levels=np.linspace(264,320,15).tolist()
temp_diff_levels=np.linspace(-4,4,16).tolist()
precip_levels=np.linspace(0.1,6,15)
precip_diff_levels=np.linspace(-4,4,16).tolist()

sample_file=np.load('/store/c2sm/pr04/jvergara/meteoswiss_data/grid/season_means/TmaxD_2006_SON.npy')
n_years=len(years)
arrays_shape=(4,n_years,sample_file.shape[0],sample_file.shape[1])
obs_temps=np.zeros(arrays_shape)
model_temps=np.zeros(arrays_shape)
obs_prec=np.zeros(arrays_shape)
model_prec=np.zeros(arrays_shape)



data_path='/store/c2sm/pr04/jvergara/meteoswiss_data/grid/season_means/'
season=jle.seasons[0]
for iseason in range(4):
    season=jle.seasons[iseason]
    print(season)
# =============================================================================
#         TEMPERATURE
# =============================================================================
    for iyear in range(n_years):
        ds=Dataset(files_path+'lffd'+year+'_'+season+'_regrided_meteoswiss_1k.nc')
        model_data=ds.variables['T_2M'][0,]
        model_temps[iseason,iyear,:,:]=model_data
        
        obs_data=np.load(data_path+'TabsD_'+year+'_'+season+'.npy')+273.15
        obs_temps[iseason,iyear,:,:]=obs_data
# =============================================================================
#         PRECIPITATION
# =============================================================================

        try:
            model_data=ds.variables['TOT_PREC'][0,]*24
        except:
            model_data=ds.variables['TOT_PR'][0,]*3600*24

        model_prec[iseason,iyear,:,:]=model_data
        
        obs_data=np.load(data_path+'RhiresD_'+year+'_'+season+'.npy')
        obs_prec[iseason,iyear,:,:]=obs_data
#%%


bias_temp=model_temps-obs_temps
#bias_prec[]

bias_temp_annual_mean=np.nanmean(bias_temp,axis=1)


#%%
bias_prec=model_prec-eobs_prec
#bias_prec[]
bias_prec_annual_mean=np.nanmean(bias_prec,axis=1)

#%%

sample_nc=Dataset('/store/c2sm/pr04/jvergara/meteoswiss_data/grid/RdisaggH_ch01r.swisscors_latlon.nc')

X=sample_nc.variables['lon'][:]
Y=sample_nc.variables['lat'][:]


sample_nc=Dataset(run_path+'1h/lffd20060613120000.nc')
lat_bounds=[sample_nc.variables['lat'][:].min(),sample_nc.variables['lat'][:].max()]
lon_bounds=[sample_nc.variables['lon'][:].min(),sample_nc.variables['lon'][:].max()]

#ylims=[Y[~total_mask].min(),Y[~total_mask].max()]
#xlims=[X[~total_mask].min(),X[~total_mask].max()]
#%%
plt.figure(figsize=(18,14))
for iseason in range(4):
    season=jle.seasons[iseason]
    print(season)
    iplot=iseason+1
    plt.subplot(2,2,iplot)
    plt.title(season)


    jle.Quick_plot(bias_temp_annual_mean[iseason] ,ini_year+'-'+end_year+' '+season+' MB %1.3f K'%(np.nanmean(bias_temp_annual_mean[iseason])),
                   levels=temp_diff_levels,latitudes=Y,longitudes=X,
                   cmap=plt.cm.RdBu_r,extend=1,new_fig=0,cb_format='%1.2f',cb_label='K',lat_bounds=lat_bounds,lon_bounds=lon_bounds,projection='rot_pol')
plt.savefig(plots_folder+'High_res_seasonal_temperature_biases_'+name+'.png')
#%%
plt.figure(figsize=(18,14))
for iseason in range(4):
    season=jle.seasons[iseason]
    print(season)
    iplot=iseason+1
    plt.subplot(2,2,iplot)
    plt.title(season)


    jle.Quick_plot(bias_prec_annual_mean[iseason] ,ini_year+'-'+end_year+' '+season+' MB %1.3f mm/h'%(np.nanmean(bias_prec_annual_mean[iseason])),
                   levels=precip_diff_levels,latitudes=Y,longitudes=X,
                   cmap=plt.cm.RdBu,extend=1,new_fig=0,cb_format='%1.2f',cb_label='mm/day',lat_bounds=lat_bounds,lon_bounds=lon_bounds,projection='rot_pol')

plt.savefig(plots_folder+'High_res_seasonal_precipitation_biases_'+name+'.png')



