#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 14:51:47 2018

@author: jvergara
"""
import matplotlib 
matplotlib.use('Agg')
import sys
sys.path.append('/users/jvergara/python_code')
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


from define_parameters import pspc_data_folder,year, plots_folder, initial_final_day_index_EOBS
from define_parameters import output_path as files_path



os.chdir(files_path)





eobs_precip=Dataset('/store/c2sm/pr04/jvergara/EOBS/rr_0.25deg_reg_v17.0.nc')

eobs_tmean=Dataset('/store/c2sm/pr04/jvergara/EOBS/tg_0.25deg_reg_v17.0.nc')

eobs=Dataset('/store/c2sm/pr04/jvergara/EOBS/rr_0.25deg_reg_v17.0.nc')


    
#%%
levels=np.linspace(0,9,10)

for month in jle.months_number_str:
    print (month)
    
# =============================================================================
#   Precipitation
# =============================================================================
    plt.figure(figsize=(20,20))
    print('PRECIPITATION EVALUATION')
    
    ds=Dataset(files_path+'lffd2006%s_%s.nc'%(month,jle.month_names[int(month)-1]))
    
    domain_mask=ds.variables['RELHUM_2M'][:].mean(axis=(0,1))==0
    
    s,e=initial_final_day_index_EOBS(year,month)
    eobs_mm=eobs_precip.variables['rr'][s:e].mean(axis=0)
    units=eobs_precip.variables['rr'].units
    X,Y=np.meshgrid(ds.variables['longitude'][:],ds.variables['latitude'][:])
    eobs_mask=np.copy(eobs_mm.mask)
    total_mask=np.logical_or(eobs_mask,domain_mask)
    eobs_mm[total_mask]=np.nan
    
    model_mm=ds.variables['TOT_PREC'][:].mean(axis=0)
    model_mm[total_mask]=np.nan
    
    plt.subplot(221)
    jle.Quick_plot(eobs_mm,'Precipitation EOBS '+year+' '+month,latitudes=Y,longitudes=X,levels=levels,cb_label=units,new_fig=False,cb_format='%1.1f')
    plt.subplot(222)
    jle.Quick_plot(model_mm*24,'Model ',latitudes=Y,longitudes=X,levels=levels,cb_label=units,new_fig=False,cb_format='%1.1f')
    
    dif_levels=jle.from_levels_to_diflevels(levels,fraction=0.5)
    dif=model_mm*24-eobs_mm
    plt.subplot(223)
    jle.Quick_plot(dif,'Difference model-EOBS ',latitudes=Y,longitudes=X,levels=dif_levels,cmap=plt.cm.RdBu,cb_label=units,new_fig=False,cb_format='%1.1f')
    data=dif.flatten()
    data=data[~np.isnan(data)]
    plt.subplot(224)
    plt.hist(data,bins=200)
    plt.title('Diff histogram. Mean_bias=%1.2f %s'%(data.mean(),units))
#    plt.yscale('log')
    plt.savefig(plots_folder+'Precipitation_evaluation_%s.png'%jle.month_names[int(month)-1])
    
    
    
    
    
    
# =============================================================================
#     Mean Temperature
# =============================================================================
    print('SURFACE TEMPERATURE EVALUATION')
    levels=np.linspace(258,300,15).tolist()


    plt.figure(figsize=(20,20))
    
    ds=Dataset(files_path+'lffd2006%s_%s.nc'%(month,jle.month_names[int(month)-1]))
    
    domain_mask=ds.variables['RELHUM_2M'][:].mean(axis=(0,1))==0
    
    s,e=initial_final_day_index_EOBS(year,month)
    eobs_mm=eobs_tmean.variables['tg'][s:e].mean(axis=0)+273.15
    units=ds.variables['T_2M'].units
    X,Y=np.meshgrid(ds.variables['longitude'][:],ds.variables['latitude'][:])
    eobs_mask=np.copy(eobs_mm.mask)
    total_mask=np.logical_or(eobs_mask,domain_mask)
    eobs_mm[total_mask]=np.nan
    
    model_mm=ds.variables['T_2M'][:].mean(axis=(0,1))
    model_mm[total_mask]=np.nan
    
    plt.figure(figsize=(20,20))
    plt.subplot(221)
    jle.Quick_plot(eobs_mm,'Temperature EOBS '+year+' '+month,latitudes=Y,longitudes=X,levels=levels,cb_label=units,new_fig=False,cmap=plt.cm.gist_ncar)
    plt.subplot(222)
    jle.Quick_plot(model_mm,'Model ',latitudes=Y,longitudes=X,levels=levels,cb_label=units,new_fig=False,cmap=plt.cm.gist_ncar)
    
    dif_levels=np.linspace(-5,5,11)
    dif=model_mm-eobs_mm
    plt.subplot(223)
    jle.Quick_plot(dif,'Difference model-EOBS ',latitudes=Y,longitudes=X,levels=dif_levels,cmap=plt.cm.RdBu,cb_label=units,new_fig=False,cb_format='%1.1f')
    data=dif.flatten()
    data=data[~np.isnan(data)]
    plt.subplot(224)
    plt.hist(data,bins=200)
    plt.title('Diff histogram. Mean_bias=%1.2f %s'%(data.mean(),units))
    plt.savefig(plots_folder+'Temperature_evaluation_%s.png'%jle.month_names[int(month)-1])
