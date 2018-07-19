#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 14:51:47 2018

@author: jvergara
"""

import sys
sys.path.append('/users/jvergara/python_code')
import matplotlib
matplotlib.use('Agg')
import Jesuslib_eth as jle
import numpy as np
import matplotlib.pyplot as plt
import glob
from netCDF4 import Dataset
import time
import os
import matplotlib.animation as manimation
from pympler import muppy
all_objects = muppy.get_objects()
from pympler import summary
import pickle
import scipy
import datetime
from dateutil.relativedelta import relativedelta


from define_parameters import pspc_data_folder,year, plots_folder, initial_final_day_index_EOBS, name
from define_parameters import output_path as files_path





os.chdir(files_path)

eobs_precip=Dataset('/store/c2sm/pr04/jvergara/EOBS/rr_0.25deg_reg_v17.0.nc')

eobs_tmean=Dataset('/store/c2sm/pr04/jvergara/EOBS/tg_0.25deg_reg_v17.0.nc')

#%%

for i in range(len(jle.seasons)):
    print (jle.seasons[i])
    months=[jle.months_number_str[ind] for ind in jle.season_indexes[i]]
# =============================================================================
#   Precipitation
# =============================================================================
    plt.figure(figsize=(20,20))
    print('PRECIPITATION EVALUATION')
    levels=np.linspace(0,9,10)
    
    ds1=Dataset(files_path+'lffd%s%s_%s.nc'%(year,months[0],jle.month_names[int(months[0])-1]))
    ds2=Dataset(files_path+'lffd%s%s_%s.nc'%(year,months[1],jle.month_names[int(months[1])-1]))
    ds3=Dataset(files_path+'lffd%s%s_%s.nc'%(year,months[2],jle.month_names[int(months[2])-1]))
    
    if ds1.variables['RELHUM_2M'][:].ndim==4:
        domain_mask=ds1.variables['RELHUM_2M'][:].mean(axis=(0,1))==0
    else:
        domain_mask=ds1.variables['RELHUM_2M'][:].mean(axis=(0))==0
    
    s1,e1=initial_final_day_index_EOBS(year,months[0])
    s2,e2=initial_final_day_index_EOBS(year,months[1])
    s3,e3=initial_final_day_index_EOBS(year,months[2])
    eobs_mm1=eobs_precip.variables['rr'][s1:e1]
    eobs_mm2=eobs_precip.variables['rr'][s2:e2]
    eobs_mm3=eobs_precip.variables['rr'][s3:e3]
    units=eobs_precip.variables['rr'].units
    X,Y=np.meshgrid(ds1.variables['longitude'][:],ds1.variables['latitude'][:])


    f_value=eobs_precip.variables['rr']._FillValue
    eobs_sm=np.concatenate((eobs_mm1,eobs_mm2,eobs_mm3))

    eobs_mask=(eobs_sm==f_value)
    eobs_mask=eobs_mask.sum(axis=0).astype('bool')
    eobs_sm=eobs_sm.mean(axis=0)
    

    # eobs_sm=np.concatenate((eobs_mm1,eobs_mm2,eobs_mm3)).mean(axis=0)

    # eobs_mask=np.logical_or(eobs_mm1.mean(axis=0).mask,eobs_mm2.mean(axis=0).mask,eobs_mm3.mean(axis=0))
    # eobs_mask=np.logical_or(eobs_mask,eobs_sm<0)
    total_mask=np.logical_or(eobs_mask,domain_mask)
    
    
    eobs_sm[total_mask]=np.nan
    
    model_mm1=ds1.variables['TOT_PREC'][:]
    model_mm2=ds2.variables['TOT_PREC'][:]
    model_mm3=ds3.variables['TOT_PREC'][:]

    model_sm=np.concatenate((model_mm1,model_mm2,model_mm3)).mean(axis=0)
    model_sm[total_mask]=np.nan
    
    plt.subplot(221)
    jle.Quick_plot(eobs_sm,'Precipitation EOBS '+year+' '+jle.seasons[i],latitudes=Y,longitudes=X,levels=levels,cb_label=units,new_fig=False,cb_format='%1.1f')
    plt.subplot(222)
    jle.Quick_plot(model_sm*24,'Model ',latitudes=Y,longitudes=X,levels=levels,cb_label=units,new_fig=False,cb_format='%1.1f')
    
    dif_levels=jle.from_levels_to_diflevels(levels,fraction=0.5)
    dif=model_sm*24-eobs_sm
    plt.subplot(223)
    jle.Quick_plot(dif,'Difference model-EOBS ',latitudes=Y,longitudes=X,levels=dif_levels,cmap=plt.cm.RdBu,cb_label=units,new_fig=False,cb_format='%1.1f')
    data=dif.flatten()
    data=data[~np.isnan(data)]
    plt.subplot(224)
    plt.hist(data,bins=200)
    plt.title('Diff histogram. Mean_bias=%1.2f %s'%(data.mean(),units))
    
    plt.savefig(plots_folder+name+'_precipitation_evaluation_%s.png'%jle.seasons[i])
    
#%%
    
    
    
    
# =============================================================================
#     Mean Temperature
# =============================================================================
    print('SURFACE TEMPERATURE EVALUATION')
#    levels=np.linspace(260,300,10)
    levels=np.linspace(258,300,15).tolist()


    plt.figure(figsize=(20,20))
    
    ds1=Dataset(files_path+'lffd%s%s_%s.nc'%(year,months[0],jle.month_names[int(months[0])-1]))
    ds2=Dataset(files_path+'lffd%s%s_%s.nc'%(year,months[1],jle.month_names[int(months[1])-1]))
    ds3=Dataset(files_path+'lffd%s%s_%s.nc'%(year,months[2],jle.month_names[int(months[2])-1]))
    
    if ds1.variables['RELHUM_2M'][:].ndim==4:
        domain_mask=ds1.variables['RELHUM_2M'][:].mean(axis=(0,1))==0
    else:
        domain_mask=ds1.variables['RELHUM_2M'][:].mean(axis=(0))==0
    
    s1,e1=initial_final_day_index_EOBS(year,months[0])
    s2,e2=initial_final_day_index_EOBS(year,months[1])
    s3,e3=initial_final_day_index_EOBS(year,months[2])
    eobs_mm1=eobs_tmean.variables['tg'][s1:e1]+273.15
    eobs_mm2=eobs_tmean.variables['tg'][s2:e2]+273.15
    eobs_mm3=eobs_tmean.variables['tg'][s3:e3]+273.15

    # eobs_sm=np.concatenate((eobs_mm1,eobs_mm2,eobs_mm3)).mean(axis=0)
    f_value=eobs_tmean.variables['tg']._FillValue
    eobs_sm=np.concatenate((eobs_mm1,eobs_mm2,eobs_mm3))

    eobs_mask=(eobs_sm==f_value)
    eobs_mask=eobs_mask.sum(axis=0).astype('bool')
    eobs_sm=eobs_sm.mean(axis=0)
    

    
    
    units=ds1.variables['T_2M'].units
    X,Y=np.meshgrid(ds1.variables['longitude'][:],ds1.variables['latitude'][:])


#    eobs_mask=np.logical_or(eobs_mm1.mean(axis=0).mask,eobs_mm2.mean(axis=0).mask,eobs_mm3.mean(axis=0).mask)
#    eobs_mask=np.logical_or(eobs_mm1.mask.mean(axis=0),eobs_mm2.mask.mean(axis=0),eobs_mm3.mask.mean(axis=0))
    # eobs_mask=np.logical_or(eobs_mm1.mean(axis=0).mask,eobs_mm2.mean(axis=0).mask,eobs_mm3.mean(axis=0))

    # eobs_mask=np.logical_or(eobs_mask,eobs_sm<0)
#    total_mask=np.logical_or(eobs_mask,domain_mask)

#    eobs_mask=np.copy(eobs_mm1.mask.mean(axis=0)*eobs_mm2.mask.mean(axis=0)*eobs_mm3.mask.mean(axis=0))
    total_mask=np.logical_or(eobs_mask,domain_mask)
    eobs_sm[total_mask]=np.nan
    
    
        
    model_mm1=ds1.variables['T_2M'][:]
    model_mm2=ds2.variables['T_2M'][:]
    model_mm3=ds3.variables['T_2M'][:]

    model_sm=np.concatenate((model_mm1,model_mm2,model_mm3))
    if model_sm.ndim==4:
        model_sm=model_sm.mean(axis=(0,1))
    else:
        model_sm=model_sm.mean(axis=(0))
        
    model_sm[total_mask]=np.nan

    
#    model_mm=ds.variables['T_2M'][:].mean(axis=(0,1))
#    model_mm[total_mask]=np.nan
    
    plt.figure(figsize=(20,20))
    plt.subplot(221)
    jle.Quick_plot(eobs_sm,'Temperature EOBS '+year+' '+jle.seasons[i],latitudes=Y,longitudes=X,levels=levels,cb_label=units,new_fig=False,cmap=plt.cm.gist_ncar,cb_format='%1.1f')
    plt.subplot(222)
    jle.Quick_plot(model_sm,'Model ',latitudes=Y,longitudes=X,levels=levels,cb_label=units,new_fig=False,cmap=plt.cm.gist_ncar,cb_format='%1.1f')
#    jle.Quick_plot(mean.mean(axis=(0,1)),'Model ',latitudes=Y,longitudes=X,levels=levels,cb_label=units,new_fig=False)
    
    dif_levels=np.linspace(-5,5,11)
    dif=model_sm-eobs_sm
    plt.subplot(223)
    jle.Quick_plot(dif,'Difference model-EOBS ',latitudes=Y,longitudes=X,levels=dif_levels,cmap=plt.cm.RdBu_r,cb_label=units,new_fig=False,cb_format='%1.1f')
    data=dif.flatten()
    data=data[~np.isnan(data)]
    plt.subplot(224)
    plt.hist(data,bins=200)
    plt.title('Diff histogram. Mean_bias=%1.2f %s'%(data.mean(),units))
#    plt.yscale('log')
    plt.savefig(plots_folder+name+'_temperature_evaluation_%s.png'%jle.seasons[i])
