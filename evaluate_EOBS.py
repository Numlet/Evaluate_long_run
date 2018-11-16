from define_parameters import *
import glob
from netCDF4 import Dataset
import matplotlib.pyplot as plt

from define_parameters import pspc_data_folder,year, plots_folder, initial_final_day_index_EOBS, name
from define_parameters import output_path as files_path

#files_folder='/store/c2sm/pr04/jvergara/SATELLITE/CMSAF/'



eobs_precip=Dataset('/store/c2sm/pr04/jvergara/EOBS/rr_0.25deg_reg_v17.0.nc')

eobs_tmean=Dataset('/store/c2sm/pr04/jvergara/EOBS/tg_0.25deg_reg_v17.0.nc')


monthly_mean_precip=[]
monthly_mean_temperature=[]
monthly_mask_precip=[]
monthly_mask_temperature=[]

for i in range(12):
    print (i)
    month=jle.months_number_str[i]

    s,e=initial_final_day_index_EOBS(year,month)
    monthly_mean_precip.append(eobs_precip.variables['rr'][s:e].mean(axis=0))
    eobs_mask=eobs_precip.variables['rr'][s:e].mean(axis=0).mask
    monthly_mask_precip.append(eobs_mask)

    monthly_mean_temperature.append((eobs_tmean.variables['tg'][s:e]+273.15).mean(axis=0))
    eobs_mask=eobs_tmean.variables['tg'][s:e].mean(axis=0).mask
    monthly_mask_temperature.append(eobs_mask)
#%%
monthly_mean_temperature=np.array(monthly_mean_temperature)
monthly_mean_precip=np.array(monthly_mean_precip)
monthly_mask_temperature=np.array(monthly_mask_temperature)
monthly_mask_precip=np.array(monthly_mask_precip)



precip_dict={}
temperature_dict={}
precip_mask_dict={}
temperature_mask_dict={}

for i in range(len(jle.seasons)):
    print(jle.seasons[i])
    print(jle.season_indexes[i])
    precip_dict[jle.seasons[i]]=monthly_mean_precip[jle.season_indexes[i],:,:].mean(axis=0)
    temperature_dict[jle.seasons[i]]=monthly_mean_temperature[jle.season_indexes[i],:,:].mean(axis=0)
    precip_mask_dict[jle.seasons[i]]=monthly_mean_precip[jle.season_indexes[i],:,:].mean(axis=0)
    temperature_mask_dict[jle.seasons[i]]=monthly_mask_temperature[jle.season_indexes[i],:,:].sum(axis=0).astype('bool')
    precip_mask_dict[jle.seasons[i]]=monthly_mask_precip[jle.season_indexes[i],:,:].sum(axis=0).astype('bool')


#%%
season=jle.seasons[0]
for season in jle.seasons:
#    if season!='JJA':continue
    try:
# =============================================================================
#         TEMPERATURE
# =============================================================================
        bias_dict={}
        corr_dict={}
        err_dict={}
        
        print(name)
        print(season)
        levels=np.linspace(264,320,15).tolist()
        ds=Dataset(output_path+'lffd'+year+'_'+season+'_regrided_EOBS.nc')
        model_data=ds.variables['T_2M'][0,]
        sample_nc=Dataset(sample_nc_path)
        lat_bounds=[sample_nc.variables['lat'][:].min(),sample_nc.variables['lat'][:].max()]
        lon_bounds=[sample_nc.variables['lon'][:].min(),sample_nc.variables['lon'][:].max()]
        
        X,Y=np.meshgrid(ds.variables['longitude'][:],ds.variables['latitude'][:])
        
        if ds.variables['RELHUM_2M'][:].ndim==4:
            domain_mask=ds.variables['RELHUM_2M'][:].mask[0,]
        else:
            domain_mask=ds.variables['RELHUM_2M'][:].mask[0,]
        
        
        eobs_mask=temperature_mask_dict[season]
        total_mask=np.logical_or(eobs_mask,domain_mask)
        model_data[total_mask]=np.nan
        ylims=[Y[~total_mask].min(),Y[~total_mask].max()]
        xlims=[X[~total_mask].min(),X[~total_mask].max()]

        
        plt.figure(figsize=(20,20))
        plt.subplot(222)        
        jle.Quick_plot(model_data,name,latitudes=Y,longitudes=X,levels=levels,cb_label='K',new_fig=False,cb_format='%1.1f',lat_bounds=ylims,lon_bounds=xlims)
        model_data.data[model_data.mask]=np.nan
        
        plt.subplot(221)        
        jle.Quick_plot(temperature_dict[season],'Temperature EOBS '+year+' '+season,latitudes=Y,longitudes=X,
                       levels=levels,cb_label='K',new_fig=False,cb_format='%1.1f',lat_bounds=ylims,lon_bounds=xlims)
        diff=model_data-temperature_dict[season]
        
        plt.subplot(223)
        jle.Quick_plot(diff ,'diff mean '+str(np.nanmean(diff)),latitudes=Y,longitudes=X,levels=np.linspace(-12,12,16),
                       cmap=plt.cm.RdBu,lat_bounds=ylims,lon_bounds=xlims,extend=1,new_fig=0,cb_format='%1.2f')
        plt.subplot(224)
        values=diff[~np.isnan(model_data)]
        plt.hist(values,bins=100,normed=1)
        plt.axvline(0,c='k',ls='--')

        plt.xlabel('bias W/m2')
        corr,bias,error=jle.Calculate_skills(model_data,temperature_dict[season])
        
        err_dict[name]=error
        bias_dict[name]=bias
        corr_dict[name]=corr**2
    
        plt.savefig(plots_folder+'Temperature_biases_EOBS_'+name+'_'+season+'.png')
        
# =============================================================================
#         PRECIPITATION
# =============================================================================
        #%%
        print(name)
        
        levels=np.linspace(0.1,5,15)
        ds=Dataset(output_path+'lffd'+year+'_'+season+'_regrided_EOBS.nc')
        model_data=ds.variables['TOT_PREC'][0,]
        sample_nc=Dataset(sample_nc_path)
        lat_bounds=[sample_nc.variables['lat'][:].min(),sample_nc.variables['lat'][:].max()]
        lon_bounds=[sample_nc.variables['lon'][:].min(),sample_nc.variables['lon'][:].max()]
        
        X,Y=np.meshgrid(ds.variables['longitude'][:],ds.variables['latitude'][:])
        
        if ds.variables['RELHUM_2M'][:].ndim==4:
            domain_mask=ds.variables['RELHUM_2M'][:].mask[0,]
        else:
            domain_mask=ds.variables['RELHUM_2M'][:].mask[0,]
        
        
        eobs_mask=precip_mask_dict[season]
        total_mask=np.logical_or(eobs_mask,domain_mask)
        model_data[total_mask]=np.nan
        ylims=[Y[~total_mask].min(),Y[~total_mask].max()]
        xlims=[X[~total_mask].min(),X[~total_mask].max()]

        
        plt.figure(figsize=(20,20))
        plt.subplot(222)        
        jle.Quick_plot(model_data*24,name,latitudes=Y,longitudes=X,levels=levels,cb_label='mm',new_fig=False,cb_format='%1.1f',lat_bounds=ylims,lon_bounds=xlims)
        model_data.data[model_data.mask]=np.nan
        
        plt.subplot(221)        
        jle.Quick_plot(precip_dict[season],'Precipitation EOBS '+year+' '+season,latitudes=Y,longitudes=X,levels=levels,cb_label='mm',
                       new_fig=False,cb_format='%1.1f',lat_bounds=ylims,lon_bounds=xlims,extend='max')
        diff=model_data*24-precip_dict[season]
        
        plt.subplot(223)
        jle.Quick_plot(diff ,'diff mean '+str(np.nanmean(diff)),latitudes=Y,longitudes=X,levels=np.linspace(-4,4,16),
                       cmap=plt.cm.RdBu,lat_bounds=ylims,lon_bounds=xlims,extend=1,new_fig=0,cb_format='%1.2f')
        plt.subplot(224)
        values=diff[~np.isnan(model_data)]
        plt.hist(values,bins=100,normed=1)
        plt.axvline(0,c='k',ls='--')

        plt.xlabel('bias W/m2')
        corr,bias,error=jle.Calculate_skills(model_data,precip_dict[season])
        
        err_dict[name]=error
        bias_dict[name]=bias
        corr_dict[name]=corr**2
    
        plt.savefig(plots_folder+'Precipitation_biases_EOBS_'+name+'_'+season+'.png')
        #%%
    except:
        print(season +' could not be evaluated')
#%%
for month in jle.months_number_str:
    try:
    #    if season!='JJA':continue
        imonth=int(month)-1
        month_name=jle.month_names[imonth]
        print(month_name)
# =============================================================================
#         TEMPERATURE
# =============================================================================
        bias_dict={}
        corr_dict={}
        err_dict={}
        
        print(name)
        levels=np.linspace(264,320,15).tolist()
        ds=Dataset(output_path+'lffd'+year+month+'_regrided_EOBS.nc')
        model_data=ds.variables['T_2M'][0,]
        sample_nc=Dataset(sample_nc_path)
        lat_bounds=[sample_nc.variables['lat'][:].min(),sample_nc.variables['lat'][:].max()]
        lon_bounds=[sample_nc.variables['lon'][:].min(),sample_nc.variables['lon'][:].max()]
        
        X,Y=np.meshgrid(ds.variables['longitude'][:],ds.variables['latitude'][:])
        
        if ds.variables['RELHUM_2M'][:].ndim==4:
            domain_mask=ds.variables['RELHUM_2M'][:].mask[0,]
        else:
            domain_mask=ds.variables['RELHUM_2M'][:].mask[0,]
        
        
        eobs_mask=monthly_mask_temperature[imonth]
        total_mask=np.logical_or(eobs_mask,domain_mask)
        model_data[total_mask]=np.nan
        ylims=[Y[~total_mask].min(),Y[~total_mask].max()]
        xlims=[X[~total_mask].min(),X[~total_mask].max()]

        
        plt.figure(figsize=(20,20))
        plt.subplot(222)        
        jle.Quick_plot(model_data,name,latitudes=Y,longitudes=X,levels=levels,cb_label='K',new_fig=False,cb_format='%1.1f',lat_bounds=ylims,lon_bounds=xlims)
        model_data.data[model_data.mask]=np.nan
        
        plt.subplot(221)        
        jle.Quick_plot(monthly_mean_temperature[imonth],'Temperature EOBS '+year+' '+month_name,latitudes=Y,longitudes=X,
                       levels=levels,cb_label='K',new_fig=False,cb_format='%1.1f',lat_bounds=ylims,lon_bounds=xlims)
        diff=model_data-monthly_mean_temperature[imonth]
        
        plt.subplot(223)
        jle.Quick_plot(diff ,'diff mean '+str(np.nanmean(diff)),latitudes=Y,longitudes=X,levels=np.linspace(-12,12,16),
                       cmap=plt.cm.RdBu,lat_bounds=ylims,lon_bounds=xlims,extend=1,new_fig=0,cb_format='%1.2f')
        plt.subplot(224)
        values=diff[~np.isnan(model_data)]
        plt.hist(values,bins=100,normed=1)
        plt.axvline(0,c='k',ls='--')

        plt.xlabel('bias W/m2')
        corr,bias,error=jle.Calculate_skills(model_data,monthly_mean_temperature[imonth])
        
        err_dict[name]=error
        bias_dict[name]=bias
        corr_dict[name]=corr**2
    
        plt.savefig(plots_folder+'Temperature_biases_EOBS_'+name+'_'+month_name+'.png')
        
# =============================================================================
#         PRECIPITATION
# =============================================================================
        #%%
        print(name)
        
        levels=np.linspace(0.1,5,15)
        ds=Dataset(output_path+'lffd'+year+'_'+month_name+'_regrided_EOBS.nc')
        model_data=ds.variables['TOT_PREC'][0,]
        sample_nc=Dataset(sample_nc_path)
        lat_bounds=[sample_nc.variables['lat'][:].min(),sample_nc.variables['lat'][:].max()]
        lon_bounds=[sample_nc.variables['lon'][:].min(),sample_nc.variables['lon'][:].max()]
        
        X,Y=np.meshgrid(ds.variables['longitude'][:],ds.variables['latitude'][:])
        
        if ds.variables['RELHUM_2M'][:].ndim==4:
            domain_mask=ds.variables['RELHUM_2M'][:].mask[0,]
        else:
            domain_mask=ds.variables['RELHUM_2M'][:].mask[0,]
        
        
        eobs_mask=monthly_mask_precip[imonth]
        total_mask=np.logical_or(eobs_mask,domain_mask)
        model_data[total_mask]=np.nan
        ylims=[Y[~total_mask].min(),Y[~total_mask].max()]
        xlims=[X[~total_mask].min(),X[~total_mask].max()]

        
        plt.figure(figsize=(20,20))
        plt.subplot(222)        
        jle.Quick_plot(model_data*24,name,latitudes=Y,longitudes=X,levels=levels,cb_label='mm',new_fig=False,cb_format='%1.1f',lat_bounds=ylims,lon_bounds=xlims)
        model_data.data[model_data.mask]=np.nan
        
        plt.subplot(221)        
        jle.Quick_plot(monthly_mean_precip[imonth],'Precipitation EOBS '+year+' '+month_name,latitudes=Y,longitudes=X,levels=levels,cb_label='mm',
                       new_fig=False,cb_format='%1.1f',lat_bounds=ylims,lon_bounds=xlims,extend='max')
        diff=model_data*24-monthly_mean_precip[imonth]
        
        plt.subplot(223)
        jle.Quick_plot(diff ,'diff mean '+str(np.nanmean(diff)),latitudes=Y,longitudes=X,levels=np.linspace(-4,4,16),
                       cmap=plt.cm.RdBu,lat_bounds=ylims,lon_bounds=xlims,extend=1,new_fig=0,cb_format='%1.2f')
        plt.subplot(224)
        values=diff[~np.isnan(model_data)]
        plt.hist(values,bins=100,normed=1)
        plt.axvline(0,c='k',ls='--')

        plt.xlabel('bias W/m2')
        corr,bias,error=jle.Calculate_skills(model_data,monthly_mean_precip[imonth])
        
        err_dict[name]=error
        bias_dict[name]=bias
        corr_dict[name]=corr**2
    
        plt.savefig(plots_folder+'Precipitation_biases_EOBS_'+name+'_'+month_name+'.png')


    except:
        imonth=int(month)-1
        print(jle.month_names[imonth] +' could not be evaluated')
        
