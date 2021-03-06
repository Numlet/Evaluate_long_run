import matplotlib 
matplotlib.use("Agg")
from define_parameters import *
import glob
from netCDF4 import Dataset
import matplotlib.pyplot as plt

from define_parameters import pspc_data_folder,years, plots_folder, initial_final_day_index_EOBS, name
from define_parameters import output_path as files_path

#files_folder='/store/c2sm/pr04/jvergara/SATELLITE/CMSAF/'
ini_year=str(np.array(years).astype('int').min())
end_year=str(np.array(years).astype('int').max())

eobs_data_path='/store/c2sm/pr04/jvergara/EOBS/season_means/'
sample_EOBS_file=np.load(eobs_data_path+'EOBS_temp_1970_DJF.npy')

temp_levels=np.linspace(264,320,15).tolist()
temp_diff_levels=np.linspace(-4,4,16).tolist()
precip_levels=np.linspace(0.1,6,15)
precip_diff_levels=np.linspace(-4,4,16).tolist()

n_years=len(years)
arrays_shape=(4,n_years,sample_EOBS_file.shape[0],sample_EOBS_file.shape[1])
eobs_temps=np.zeros(arrays_shape)
model_temps=np.zeros(arrays_shape)
model_temps_mask=np.zeros(arrays_shape)
eobs_temps_mask=np.zeros(arrays_shape)


eobs_prec=np.zeros(arrays_shape)
model_prec=np.zeros(arrays_shape)
model_prec_mask=np.zeros(arrays_shape)
eobs_prec_mask=np.zeros(arrays_shape)





#%%
season=jle.seasons[0]
for iseason in range(4):
    season=jle.seasons[iseason]
    print(season)
# =============================================================================
#         TEMPERATURE
# =============================================================================
    for iyear in range(n_years):
        year=years[iyear]
        ds=Dataset(files_path+'lffd'+year+'_'+season+'_regrided_EOBS.nc')
        model_data=ds.variables['T_2M'][0,]
        if ds.variables['RELHUM_2M'][:].ndim==4:
            domain_mask=ds.variables['RELHUM_2M'][:].mask[0,]
        else:
            domain_mask=ds.variables['RELHUM_2M'][:].mask[0,]
        model_temps[iseason,iyear,:,:]=model_data
        model_temps_mask[iseason,iyear,:,:]=domain_mask
        
        eobs_data=np.load(eobs_data_path+'EOBS_temp_'+year+'_'+season+'.npy')
        eobs_data_mask=np.load(eobs_data_path+'EOBS_temp_mask_'+year+'_'+season+'.npy')
        eobs_temps[iseason,iyear,:,:]=eobs_data
        eobs_temps_mask[iseason,iyear,:,:]=eobs_data_mask
    # =============================================================================
    #         PRECIPITATION
    # =============================================================================
        print(year)
        
    #        levels=np.linspace(0.1,5,15)
        ds=Dataset(files_path+'lffd'+year+'_'+season+'_regrided_EOBS.nc')
        try:
            model_data=ds.variables['TOT_PREC'][0,]
        except:
            model_data=ds.variables['TOT_PR'][0,]*3600*24
        X,Y=np.meshgrid(ds.variables['longitude'][:],ds.variables['latitude'][:])
        if ds.variables['RELHUM_2M'][:].ndim==4:
            domain_mask=ds.variables['RELHUM_2M'][:].mask[0,]
        else:
            domain_mask=ds.variables['RELHUM_2M'][:].mask[0,]
        
        model_prec[iseason,iyear,:,:]=model_data
        model_prec_mask[iseason,iyear,:,:]=domain_mask
        
        eobs_data=np.load(eobs_data_path+'EOBS_precip_'+year+'_'+season+'.npy')
        eobs_data_mask=np.load(eobs_data_path+'EOBS_precip_mask_'+year+'_'+season+'.npy')
        eobs_prec[iseason,iyear,:,:]=eobs_data
        eobs_prec_mask[iseason,iyear,:,:]=eobs_data_mask



#%%

season=jle.seasons[0]

bias_temp=model_temps-eobs_temps
#bias_prec[]
bias_temp[eobs_temps_mask.astype('bool')]=np.nan
bias_temp[model_temps_mask.astype('bool')]=np.nan

bias_temp_annual_mean=np.nanmean(bias_temp,axis=1)


#%%
bias_prec=model_prec-eobs_prec
#bias_prec[]
bias_prec[eobs_prec_mask.astype('bool')]=np.nan
bias_prec[model_prec_mask.astype('bool')]=np.nan
bias_prec_annual_mean=np.nanmean(bias_prec,axis=1)


#%%

#model_prec[eobs_prec_mask.astype('bool')]=np.nan
#model_prec[model_prec_mask.astype('bool')]=np.nan
#model_prec=np.nanmean(bias_prec,axis=1)

X,Y=np.meshgrid(ds.variables['longitude'][:],ds.variables['latitude'][:])


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
plt.savefig(plots_folder+'Seasonal_temperature_biases_'+name+'.png')
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

plt.savefig(plots_folder+'Seasonal_precipitation_biases_'+name+'.png')

