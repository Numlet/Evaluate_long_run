from define_parameters import *
import glob
from netCDF4 import Dataset
import matplotlib.pyplot as plt


files_folder='/store/c2sm/pr04/jvergara/SATELLITE/CMSAF/'

lw_files=glob.glob(files_folder+'TETmm*')
sw_files=glob.glob(files_folder+'TRSmm*')
monthly_mean_sw_in=[]
monthly_mean_sw_out=[]
monthly_mean_lw=[]
for i in range(12):
    print (i)
    lw_file=[file for file in lw_files if '%s%.2i'%(year,i+1) in file][0]
    sw_file=[file for file in sw_files if '%s%.2i'%(year,i+1) in file][0]
    print (lw_file)
    print (sw_file)
    ds=Dataset(lw_file)
    lw_mean=ds.variables['rlut'][0,]
    monthly_mean_lw.append(lw_mean)
    
    ds=Dataset(sw_file)
    sw_mean_in=ds.variables['rsdt'][0,]
    sw_mean_out=ds.variables['rsut'][0,]
    monthly_mean_sw_in.append(sw_mean_in)
    monthly_mean_sw_out.append(sw_mean_out)
    
monthly_mean_sw_in=np.array(monthly_mean_sw_in)
monthly_mean_sw_out=np.array(monthly_mean_sw_out)
monthly_mean_lw=np.array(monthly_mean_lw)

print(lw_file)


sw_net_dict={}
lw_dict={}

lw_dict['DJF']=np.mean(monthly_mean_lw[[11,0,1],:,:])
monthly_mean_sw=monthly_mean_sw_in-monthly_mean_sw_out
for i in range(len(jle.seasons)):
    print(jle.seasons[i])
    print(jle.season_indexes[i])
    lw_dict[jle.seasons[i]]=monthly_mean_lw[jle.season_indexes[i],:,:].mean(axis=0)
    sw_net_dict[jle.seasons[i]]=(monthly_mean_sw_in[jle.season_indexes[i],:,:]-monthly_mean_sw_out[jle.season_indexes[i],:,:]).mean(axis=0)




units='W/m2'
levels_lw=np.linspace(120,300,15).tolist()
levels_lw_diff=np.linspace(-50,50,16).tolist()
levels_sw=np.linspace(0,400,20).tolist()
levels_sw_diff=np.linspace(-50,50,16).tolist()

#%%
for season in jle.seasons:
#    if season!='JJA':continue
    try:
        bias_dict={}
        corr_dict={}
        err_dict={}
        
    #    for name in path_dict:
        print(name)
        print(season)
        levels=np.linspace(120,300,15).tolist()
        ds=Dataset(output_path+'lffd'+year+'_'+season+'_regrided_CMSAF.nc')
        model_data=-ds.variables['ATHB_T'][0,]
        sample_nc=Dataset(sample_nc_path)
        lat_bounds=[sample_nc.variables['lat'][:].min(),sample_nc.variables['lat'][:].max()]
        lon_bounds=[sample_nc.variables['lon'][:].min(),sample_nc.variables['lon'][:].max()]
        plt.figure(figsize=(20,20))
        plt.subplot(221)        
        jle.Quick_plot(model_data,name,metadata_dataset=ds,levels=levels_lw,lat_bounds=lat_bounds,lon_bounds=lon_bounds,new_fig=0,cb_format='%i')
        model_data.data[model_data.mask]=np.nan
        diff=model_data-lw_dict[season]
    #        diff[diff<-10000]=np.nan
        
        plt.subplot(222)        
        jle.Quick_plot(lw_dict[season],'CMSAF '+ 'Outgoing LW '+season,metadata_dataset=ds,levels=levels_lw,lat_bounds=lat_bounds,lon_bounds=lon_bounds,new_fig=0,cb_format='%i')
        
        plt.subplot(223)
        jle.Quick_plot(diff ,'longwave diff mean '+str(np.nanmean(diff)),metadata_dataset=ds,levels=levels_lw_diff,cmap=plt.cm.RdBu,lat_bounds=lat_bounds,lon_bounds=lon_bounds,extend=1,new_fig=0,cb_format='%i')
        ax=plt.subplot(224)
        values=diff[~np.isnan(model_data)]
        plt.hist(values,bins=100,normed=1)
        plt.axvline(0,c='k',ls='--')

        plt.xlabel('bias W/m2')
        corr,bias,error=jle.Calculate_skills(model_data,lw_dict[season])
        plt.text(0.75, 0.9,'Spatial correlation=%1.2f'%corr, ha='center', va='center', transform=ax.transAxes)
        plt.text(0.75, 0.85,'Mean error=%1.2f %s'%(error,units), ha='center', va='center', transform=ax.transAxes)
        plt.text(0.75, 0.8,'Mean bias=%1.2f %s'%(bias,units), ha='center', va='center', transform=ax.transAxes)
        err_dict[name]=error
        bias_dict[name]=bias
        corr_dict[name]=corr**2
    
        plt.savefig(plots_folder+'LW_biases_CMSAF_'+name+'_'+season+'.png')
        
        
        print(name)
        levels=np.linspace(0,400,20).tolist()
        ds=Dataset(output_path+'lffd'+year+'_'+season+'_regrided_CMSAF.nc')
        model_data=ds.variables['ASOB_T'][0,]
        
        lat_bounds=[sample_nc.variables['lat'][:].min(),sample_nc.variables['lat'][:].max()]
        lon_bounds=[sample_nc.variables['lon'][:].min(),sample_nc.variables['lon'][:].max()]
        plt.figure(figsize=(20,20))
        plt.subplot(221)        
        jle.Quick_plot(model_data,name,metadata_dataset=ds,levels=levels_sw,lat_bounds=lat_bounds,lon_bounds=lon_bounds,new_fig=0,cb_format='%i')
        model_data.data[model_data.mask]=np.nan
        diff=model_data-sw_net_dict[season]
    #        diff[diff<-10000]=np.nan
        
        plt.subplot(222)        
        jle.Quick_plot(sw_net_dict[season],'CMSAF net Downward SW '+season,metadata_dataset=ds,levels=levels_sw,lat_bounds=lat_bounds,lon_bounds=lon_bounds,new_fig=0,cb_format='%i')
        
        plt.subplot(223)
        jle.Quick_plot(diff ,'Shortwave diff mean '+str(np.nanmean(diff)),metadata_dataset=ds,levels=levels_sw_diff,cmap=plt.cm.RdBu_r,lat_bounds=lat_bounds,lon_bounds=lon_bounds,extend=1,new_fig=0,cb_format='%i')
        ax=plt.subplot(224)
        values=diff[~np.isnan(model_data)]
        plt.hist(values,bins=100,normed=1)
        plt.axvline(0,c='k',ls='--')

        plt.xlabel('bias W/m2')
        corr,bias,error=jle.Calculate_skills(model_data,sw_net_dict[season])
        plt.text(0.75, 0.9,'Spatial correlation=%1.2f'%corr, ha='center', va='center', transform=ax.transAxes)
        plt.text(0.75, 0.85,'Mean error=%1.2f %s'%(error,units), ha='center', va='center', transform=ax.transAxes)
        plt.text(0.75, 0.8,'Mean bias=%1.2f %s'%(bias,units), ha='center', va='center', transform=ax.transAxes)
        err_dict[name]=error
        bias_dict[name]=bias
        corr_dict[name]=corr**2
    
        plt.savefig(plots_folder+'SW_biases_CMSAF_'+name+'_'+season+'.png')
    except:
        print(season +' could not be evaluated')
#%%
for month in jle.months_number_str:
    try:
    #    if season!='JJA':continue
        imonth=int(month)-1
        month_name=jle.month_names[imonth]
        print(month_name)
        bias_dict={}
        corr_dict={}
        err_dict={}
        
    #    for name in path_dict:
        print(name)
        levels=np.linspace(120,300,15).tolist()
        ds=Dataset(output_path+'lffd'+year+month+'_regrided_CMSAF.nc')
        model_data=-ds.variables['ATHB_T'][0,]
        sample_nc=Dataset(sample_nc_path)
        lat_bounds=[sample_nc.variables['lat'][:].min(),sample_nc.variables['lat'][:].max()]
        lon_bounds=[sample_nc.variables['lon'][:].min(),sample_nc.variables['lon'][:].max()]
        plt.figure(figsize=(20,20))
        plt.subplot(221)        
        jle.Quick_plot(model_data,name,metadata_dataset=ds,levels=levels_lw,lat_bounds=lat_bounds,lon_bounds=lon_bounds,new_fig=0,cb_format='%i')
        model_data.data[model_data.mask]=np.nan
        diff=model_data-monthly_mean_lw[imonth,]
    #        diff[diff<-10000]=np.nan
        
        plt.subplot(222)        
        jle.Quick_plot(monthly_mean_lw[imonth,],'CMSAF '+ 'Outgoing LW '+month_name,metadata_dataset=ds,levels=levels_lw,lat_bounds=lat_bounds,lon_bounds=lon_bounds,new_fig=0,cb_format='%i')
        
        plt.subplot(223)
        jle.Quick_plot(diff ,'longwave diff mean '+str(np.nanmean(diff)),metadata_dataset=ds,levels=levels_lw_diff,cmap=plt.cm.RdBu,lat_bounds=lat_bounds,lon_bounds=lon_bounds,extend=1,new_fig=0,cb_format='%i')
        ax=plt.subplot(224)
        values=diff[~np.isnan(model_data)]
        plt.hist(values,bins=100,normed=1)
        plt.axvline(0,c='k',ls='--')

        plt.xlabel('bias W/m2')
        corr,bias,error=jle.Calculate_skills(model_data,monthly_mean_lw[imonth,])
        plt.text(0.75, 0.9,'Spatial correlation=%1.2f'%corr, ha='center', va='center', transform=ax.transAxes)
        plt.text(0.75, 0.85,'Mean error=%1.2f %s'%(error,units), ha='center', va='center', transform=ax.transAxes)
        plt.text(0.75, 0.8,'Mean bias=%1.2f %s'%(bias,units), ha='center', va='center', transform=ax.transAxes)
        err_dict[name]=error
        bias_dict[name]=bias
        corr_dict[name]=corr**2
    
        plt.savefig(plots_folder+'LW_biases_CMSAF_'+name+'_'+month_name+'.png')
        
        
        print(name)
        levels=np.linspace(0,400,20).tolist()
        ds=Dataset(output_path+'lffd'+year+month+'_regrided_CMSAF.nc')
        model_data=ds.variables['ASOB_T'][0,]
        
        lat_bounds=[sample_nc.variables['lat'][:].min(),sample_nc.variables['lat'][:].max()]
        lon_bounds=[sample_nc.variables['lon'][:].min(),sample_nc.variables['lon'][:].max()]
        plt.figure(figsize=(20,20))
        plt.subplot(221)        
        jle.Quick_plot(model_data,name,metadata_dataset=ds,levels=levels_sw,lat_bounds=lat_bounds,lon_bounds=lon_bounds,new_fig=0,cb_format='%i')
        model_data.data[model_data.mask]=np.nan
        diff=model_data-monthly_mean_sw[imonth,]
    #        diff[diff<-10000]=np.nan
        
        plt.subplot(222)        
        jle.Quick_plot(monthly_mean_sw[imonth,],'CMSAF net Downward SW '+month_name,metadata_dataset=ds,levels=levels_sw,lat_bounds=lat_bounds,lon_bounds=lon_bounds,new_fig=0,cb_format='%i')
        
        plt.subplot(223)
        jle.Quick_plot(diff ,'Shortwave diff mean '+str(np.nanmean(diff)),metadata_dataset=ds,levels=levels_sw_diff,cmap=plt.cm.RdBu_r,lat_bounds=lat_bounds,lon_bounds=lon_bounds,extend=1,new_fig=0,cb_format='%i')
        ax=plt.subplot(224)
        values=diff[~np.isnan(model_data)]
        plt.hist(values,bins=100,normed=1)
        plt.axvline(0,c='k',ls='--')

        plt.xlabel('bias W/m2')
        corr,bias,error=jle.Calculate_skills(model_data,monthly_mean_sw[imonth,])
#                corr,bias,error=jle.Calculate_skills(model_data[~np.isnan(model_data)],monthly_mean_temperature[imonth][~np.isnan(model_data)])
        plt.text(0.75, 0.9,'Spatial correlation=%1.2f'%corr, ha='center', va='center', transform=ax.transAxes)
        plt.text(0.75, 0.85,'Mean error=%1.2f %s'%(error,units), ha='center', va='center', transform=ax.transAxes)
        plt.text(0.75, 0.8,'Mean bias=%1.2f %s'%(bias,units), ha='center', va='center', transform=ax.transAxes)

        
        err_dict[name]=error
        bias_dict[name]=bias
        corr_dict[name]=corr**2
    
        plt.savefig(plots_folder+'SW_biases_CMSAF_'+name+'_'+month_name+'.png')
    except:
        imonth=int(month)-1
        print(jle.month_names[imonth] +' could not be evaluated')
        
