#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  9 13:44:16 2018

@author: jvergara
"""

import sys
sys.path.append('/users/jvergara/python_code')
#import matplotlib
#matplotlib.use('Agg')
import Jesuslib_eth as jle
import numpy as np
import matplotlib.pyplot as plt
import glob
#import iris
from netCDF4 import Dataset
import time
import os
import matplotlib.animation as manimation
from pympler import muppy
all_objects = muppy.get_objects()
from pympler import summary
import pickle
import scipy

from define_parameters import run_path,folder_in_path,output_path,native_grid_file,target_grid_file,year,grid_eobs,grid_cmsaf
dataset='arbitrary'
if len(sys.argv)>1:
    dataset=sys.argv[1]
if dataset=='EOBS':
    target_grid_file=grid_eobs
    folder_in_path='1h/'
if dataset=='CMSAF':
    target_grid_file=grid_cmsaf
    folder_in_path='1h_second/'
os.system('rm weights')
folder_in_path=folder_in_path[:-1]+'_mm/'

def Regrid(file,file_output_with_path,native_grid_file=native_grid_file,target_grid_file=target_grid_file,jump_past_files=0):
    do=1
    file_name_output_no_vcoord=file_output_with_path[:-3]+'_no_vcoord.nc'
    if os.path.isfile(file_output_with_path) and jump_past_files:
        do=0
        return 0
    if do:
        if not os.path.exists('weights'):
            a=os.system('cdo delname,vcoord %s %s'%(file,file_name_output_no_vcoord))
            a=os.system('cdo gencon,%s -setgrid,%s %s weights'%(target_grid_file,native_grid_file,file_name_output_no_vcoord))
            a=os.system('rm -f %s'%(file_name_output_no_vcoord))
        a=os.system('cdo delname,vcoord %s %s'%(file,file_name_output_no_vcoord))
        a=os.system('cdo remap,%s,weights -setgrid,%s %s %s'%(target_grid_file,native_grid_file,file_name_output_no_vcoord,file_output_with_path))
        os.system('rm -f %s'%(file_name_output_no_vcoord))
        return a


#%%
files=glob.glob(run_path+folder_in_path+'lffd%s*nc'%year)
files=np.sort(files)
print('\n\nFiles found to regrid:\n\n')
print(files)
#%%
import time
import multiprocessing




while True:   
    t1=time.time()
    processes=1
    output=output_path
    list_of_chunks=np.array_split(files,len(files)/processes+1)
    start=time.time()
    
    out_files={}
    for chunk in list_of_chunks:
        jobs=[]
        for file in chunk:
            print(file)
            file_name=file.split('/')[-1]
            file_name_output=file_name[:-3]+'_regrided_'+dataset+'.nc'
            file_output_with_path=output+file_name_output
            out_files[file_output_with_path]=file
#            print(output+file_name_output)
            keywords={'jump_past_files':0}
            p = multiprocessing.Process(target=Regrid, args=(file,file_output_with_path),kwargs=keywords)
            print (file,p)
            jobs.append(p)
            p.start()
        for job in jobs:
            job.join()
    
    
    
    t2=time.time()
    print(t2-t1)
    break
    



#        a=os.system('cdo delname,vcoord %s %s'%(file,file_output_with_path_no_vcoord))
#        a=os.system('cdo remapcon,%s -setgrid,%s %s %s'%(grid_12km,grid_2km,file_output_with_path_no_vcoord,file_output_with_path))
#        a=os.system('rm -f %s'%(file_output_with_path_no_vcoord))

if os.path.exists('weights'):
    os.system('rm -rf weights')
    
    
